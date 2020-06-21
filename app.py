import numpy as np
from flask import Flask, jsonify, request, render_template
import requests
import os
from PIL import Image
import googleapiclient.discovery

def predict_json(project, model, instances, version=None):
    service = googleapiclient.discovery.build('ml', 'v1')

    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)
    
    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']

def read_image(file):
    # img = Image.open(request.files['file'])
    img = Image.open(file)
    img = img.resize((150, 150))
    x = np.array(img)
    print(x.shape)
    x = np.expand_dims(x, axis=0)
    return x

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'bangkit-makeup-e913a86923af.json'

app = Flask(__name__)
# 'bangkit-makeup-e913a86923af.json'

@app.route('/', methods=['GET', 'POST'])
def index():
    #Main Page
    return render_template('index.html')
    
@app.route('/predict', methods=['GET', 'POST'])
def home():
    img = read_image(request.files['file'])
# UNCOMMENT THIS TO GET MODEL 1:
    """" 
    project_name = 'bangkit-makeup'
    model_name = 'makeup_test_model'
    version = 'v1'
    output_dense = 'dense_3'
    threshold = 0.5
    """""
# UNCOMMENT THIS TO GET MODEL 2:

    project_name = 'bangkit-makeup'
    model_name = 'bangkit_model_final_v2'
    version = 'v2'
    output_dense = 'dense_7' 
    threshold = 0.04


    print(str(project_name)+' '+str(model_name)+' '+str(version))
    get_prediction = predict_json(project_name, model_name, img.tolist(), version) 
#(, 'makeup_test_model', img.tolist(), 'v1')

    pred_dict = get_prediction[0]
    print("PRED DICT")
    print(pred_dict)
    pred = pred_dict[output_dense][0]
    class_one = pred > threshold
    return 'No Makeup!' if class_one else 'Makeup!'

if __name__ == '__main__':
    app.run(debug = True)
