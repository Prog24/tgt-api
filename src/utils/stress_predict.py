import pickle
import spacy
import numpy as np
import os

class StressPredict:
  def getVector(words, model):
    resultVectors = []
    for word in words:
      tokens = model(word)
      wordVectors = []
      count = 0
      for token in tokens:
        if not (np.all(token.vector == 0)):
          wordVectors.append(token.vector)
          count += 1
      if not count == 0:
        wordVectors = np.array(wordVectors)
        resultVectors.append(np.mean(wordVectors, axis=0))
    if len(resultVectors) == 0:
      # 1つもベクトル化出来なかった時
      return np.zeros(300)
    else:
      resultVectors = np.array(resultVectors)
      return np.mean(resultVectors, axis=0)

  def predict_stress_level(searchData):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    pred_model_path = os.path.join(dir_path, 'trained_data/stress_loc_rf.pkl')
    type_pred_model_path = os.path.join(dir_path, 'trained_data/stress_loc_rf_type.pkl')
    jp_model = spacy.load('ja_core_news_md')
    en_model = spacy.load('en_core_web_sm')
    with open(pred_model_path, 'rb') as f:
      pred_model = pickle.load(f)
    with open(type_pred_model_path, 'rb') as f:
      type_pred_model = pickle.load(f)
    
    out_data = {}
    for data in searchData:
      locationNameVector = StressPredict.getVector(data['locationName'], jp_model)
      locationTypesVector = StressPredict.getVector(data['locationType'], en_model)
      if np.all(locationNameVector == 0):
        res = type_pred_model.predict([locationTypesVector])
      else:
        returnVector = locationNameVector.tolist() + locationTypesVector.tolist()
        res = pred_model.predict([returnVector])
      out_data[data['locationName'][0]] = res[0]
    return out_data