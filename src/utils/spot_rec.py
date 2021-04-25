import os
import pickle
import spacy
import numpy as np

class SpotRec:
  # StressPredict用
  def getWordVector(words, spacyModel):
    resultVectors = []
    for word in words:
      tokens = spacyModel(word)
      wordVectors = []
      for token in tokens:
        if token.has_vector:
          wordVectors.append(token.vector)
      if not len(wordVectors) == 0:
        wordVectors = np.array(wordVectors)
        resultVectors.append(np.mean(wordVectors, axis=0))
    if len(resultVectors) == 0:
      return np.zeros(300)
    else:
      resultVectors = np.array(resultVectors)
      return np.mean(resultVectors, axis=0)
  # HappyPredict用
  def getHappyWords(bow, username, count):
    return set(bow[bow['userID'] == username].sort_values('rating', ascending=False).head(count)['word'])
  def getUserVector(bow, username, spacyModel):
    happyWords = SpotRec.getHappyWords(bow, username, 20)
    out_vec = []
    for word in happyWords:
      token = spacyModel(word)
      if token.has_vector:
        out_vec.append(token.vector)
    out_vec = np.array(out_vec)
    return np.mean(out_vec, axis=0)
  def getSpotsVector(locations, spacyModel):
    location_review_vec = {}
    for key in locations:
      review_vec = []
      if 'reviews' in locations[key]['result']:
        for review in locations[key]['result']['reviews']:
          tokens = spacyModel(review['text'])
          for token in tokens:
            if token.pos_ in ['NOUN', 'VERB'] and token.has_vector:
              review_vec.append(token.vector)
      if len(review_vec) > 0:
        review_vec = np.array(review_vec)
        review_vec = np.mean(review_vec, axis=0)
        location_review_vec[key] = review_vec
    return location_review_vec
  def cos_sim(v1, v2):
    sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    if sim == np.nan:
      return 0
    return float(sim)

  def pred_spot_score(name, locations):
    jp_model = spacy.load('ja_core_news_md')
    en_model = spacy.load('en_core_web_sm')
    dir_path = os.path.dirname(os.path.abspath(__file__))
    pred_model_path = os.path.join(dir_path, 'trained_data/stress_loc_rf.pkl')
    type_pred_model_path = os.path.join(dir_path, 'trained_data/stress_loc_rf_type.pkl')
    bow_path = os.path.join(dir_path, 'trained_data/bow.pkl')
    with open(pred_model_path, 'rb') as f:
      pred_model = pickle.load(f)
    with open(type_pred_model_path, 'rb') as f:
      type_pred_model = pickle.load(f)
    with open(bow_path, 'rb') as f:
      bow = pickle.load(f)
    # StressPredict
    stress_pred_out = {}
    for key in locations:
      locationNameVector = SpotRec.getWordVector(locations[key]['result']['name'], jp_model)
      locationTypesVector = SpotRec.getWordVector(locations[key]['result']['types'], en_model)
      if np.all(locationNameVector == 0):
        stressPredict = type_pred_model.predict([locationTypesVector])
      else:
        inputVector = locationNameVector.tolist() + locationTypesVector.tolist()
        stressPredict = pred_model.predict([inputVector])
      stress_pred_out[key] = stressPredict[0]
    # HappyPredict
    userVector = SpotRec.getUserVector(bow, name, jp_model)
    location_similarity = {}
    locationVector = SpotRec.getSpotsVector(locations, jp_model)
    for key in locationVector:
      location_similarity[key] = SpotRec.cos_sim(userVector, locationVector[key]) * 7
    out_score = {}
    for key in locations:
      if key in location_similarity:
        out_score[locations[key]['result']['name']] = (location_similarity[key] + stress_pred_out[key]) / 2
      else:
        out_score[locations[key]['result']['name']] = stress_pred_out[key]
    return out_score
