from flask import Flask
from flask import jsonify
import os
import base64
from PIL import Image
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from matplotlib.image import imread
from main import *
from waitress import serve

model = keras.models.load_model('./model/my_model.h5')

app = Flask(__name__, static_url_path='/static')

@app.route('/train')
def train():
	train_model(1000)

@app.route('/')
def home():
	return app.send_static_file('index.html')

@app.route('/prediction', methods = ['POST'])
def prediction():
	model = keras.models.load_model('./model/my_model.h5')

	img_data = request.get_json(silent=True)['base64']
	with open("./uploads/prediction.jpg", "wb") as fh:
		fh.write(base64.b64decode(img_data))
		img = Image.open("./uploads/prediction.jpg").convert('L')
		img = img.resize((28, 28), Image.ANTIALIAS)
		img.save('./uploads/prediction_scaled.jpg')

	img = imread('./uploads/prediction_scaled.jpg')
	prediction = predict(model, img)

	return jsonify(
        prediction=int(prediction),
    )



serve(app, host='0.0.0.0', port=5000)

