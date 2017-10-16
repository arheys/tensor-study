import nltk
import sys
import unicodedata
from flask import Flask
from flask import request
from flask import jsonify
import tensorflow as tf
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from nltk.stem.lancaster import LancasterStemmer

import numpy as np

application = Flask(__name__)

host = '127.0.0.1'
port = 9001

tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(unichr(i)).startswith('P'))
stemmer = LancasterStemmer()

def remove_punctuation(text):
    return text.translate(tbl)

def get_tf_record(sentence):
    global words
    # remove any punctuation from the sentence
    sentence = remove_punctuation(sentence)
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return (np.array(sentence_words))





def get_prediction(txt):
    text = get_tf_record(txt)
    export_dir = 'model'
    channel = implementations.insecure_channel(host, port)
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    request = predict_pb2.PredictRequest()

    request.model_spec.name = 'model.tflearn'

    request.model_spec.signature_name = 'predict'

    request.inputs['input'].CopyFrom(
        tf.contrib.util.make_tensor_proto(text))
    result = stub.Predict(request, 10.0)
    prediction = np.array(result.outputs['scores'].float_val)
    return prediction

@application.route('/predict', methods=['POST'])
def predict():
    res = request.get_json()
    return jsonify(get_prediction(res['text']))



if __name__ == "__main__":
    application.run()