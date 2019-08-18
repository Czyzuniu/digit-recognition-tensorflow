from __future__ import absolute_import, division, print_function, unicode_literals
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

def plot():

	#We scale these values to a range of 0 to 1 before feeding to the neural network model.
	#For this, we divide the values by 255. 
	#It's important that the training set and the testing set are preprocessed in the same way:

	train_images = train_images / 255.0
	test_images = test_images / 255.0

	plt.figure(figsize=(10,10))
	for i in range(25):
	    plt.subplot(5,5,i+1)
	    plt.xticks([])
	    plt.yticks([])
	    plt.grid(True)
	    plt.imshow(train_images[i], cmap=plt.cm.binary)
	    plt.xlabel(train_labels[i])
	plt.show()

def train_model(epochs):
	model = keras.Sequential([
	    keras.layers.Flatten(input_shape=(28, 28)),
	    keras.layers.Dense(128, activation=tf.nn.relu),
	    keras.layers.Dense(10, activation=tf.nn.softmax)
	])

	model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

	model.fit(train_images, train_labels, epochs=epochs)

	model.save('./model/my_model.h5')

	return model

def check_accuracy(model):
	test_loss, test_acc = model.evaluate(test_images, test_labels)
	print('Test accuracy:', test_acc)

def predict(model,img):
	img = (np.expand_dims(img,0))
	predictions_single = model.predict(img)
	return np.argmax(predictions_single[0])
