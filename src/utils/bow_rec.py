import pickle
import spacy
import numpy as np
import os
from gensim.models.word2vec import Word2Vec

class BowRec:
  def getHappyWords(bow, model, user, count):
    tmp_df = bow[bow['userID'] == user]
    tmp_df = tmp_df.sort_values('rating', ascending=False)
    tmp_df = tmp_df.reset_index(drop=True)
    happyWords = []
    c = 0
    for word, rating in zip(tmp_df['word'], tmp_df['rating']):
      if (c < count) and (word in model.wv.vocab):
        happyWords.append(word)
        c+=1
    return happyWords

  def getWordVector(words, model):
    resultVectors = []
    for word in words:
      if word in model.wv.vocab:
        resultVectors.append(model.wv[word])
    if len(resultVectors) == 0:
      return np.zeros(50)
    else:
      resultVectors = np.array(resultVectors)
      return np.mean(resultVectors, axis=0)
  
  def getSentenceVector(sentence, nlp, model):
    tokens = nlp(sentence)
    resultVectors = []
    for token in tokens:
      if token.lemma_ in model.wv.vocab:
        resultVectors.append(model.wv[token.lemma_])
    if len(resultVectors) == 0:
      return np.zeros(50)
    else:
      resultVectors = np.array(resultVectors)
      return np.mean(resultVectors, axis=0)
  def cos_sim(v1, v2):
    sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    if sim == np.nan:
      print('true')
      return 0
    else:
      return float(sim)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
  def predict(name, locations):
    nlp = spacy.load('ja_core_news_md')
    # load word2vec model
    dir_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(dir_path, '../../word2vec-model/word2vec.gensim.model')
    model = Word2Vec.load(model_path)
    # load HappyRecTable
    dir_path = os.path.dirname(os.path.abspath(__file__))
    bow_path = os.path.join(dir_path, 'trained_data/bow.pkl')
    with open(bow_path, 'rb') as f:
      bow = pickle.load(f)
    happyWords = BowRec.getHappyWords(bow, model, name, 10)
    happyWordsVector = BowRec.getWordVector(happyWords, model)
    # ユーザのhappyWordsVectorとそれぞれのスポットのベクトルの類似度を求める
    location_similarity = {}
    location_vector = {}
    for key in locations:
      if ('reviews' in locations[key]['result']):
        location_similarity[locations[key]['result']['name']] = 0
        # location_vector[locations[key]['result']['name']] = np.zeros((50,), dtype='float32')
        tmp_vec = np.zeros((50,), dtype='float32')
        count = 0
        for review in locations[key]['result']['reviews']:
          if not len(review['text']) == 0:
            tmp_vec = np.add(tmp_vec, BowRec.getSentenceVector(review['text'], nlp, model))
            count += 1
        if not (np.all(tmp_vec == 0)):
          tmp_vec = tmp_vec / count
        if np.all(tmp_vec == 0):
          location_similarity[locations[key]['result']['name']] = 0
        else:
          location_similarity[locations[key]['result']['name']] = BowRec.cos_sim(happyWordsVector, tmp_vec) * 7
    return location_similarity