# -*- coding: utf-8 -*-
"""Autoencoder for dimensionality reduction and image denoising.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a8qFCr4L9TChDVWi-ByfFdMT5aUgugi_

# Autoencoders for Image compression
"""

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from tensorflow.keras import models,layers

"""## Data Preparation"""

#load the MNIST dataset
(xtrain,ytrain),(xtest,ytest) = mnist.load_data()
print(xtrain.shape)
print(xtest.shape)

xtrain = xtrain/255
xtest = xtest/255

print(xtrain.shape)
print(xtest.shape)
xtrain = xtrain.reshape(60000,28*28)
xtest = xtest.reshape(10000,28*28)
print(xtrain.shape)
print(xtest.shape)

"""## Modelling"""

# Encoder
input_layer = layers.Input(shape=(784,))
dense1 = layers.Dense(128,activation='relu')(input_layer)

dense2 = layers.Dense(64,activation='relu')(dense1)

# Decoder
dense3 = layers.Dense(128,activation='relu')(dense2)
output_layer = layers.Dense(784,activation='sigmoid')(dense3)
model = models.Model(input_layer,output_layer)
model.summary()

model.compile(optimizer='adam',loss='binary_crossentropy')
model.fit(xtrain,xtrain,epochs=30,batch_size=128,shuffle=True,validation_data=(xtest,xtest))

encoder = models.Model(input_layer,dense2)
encoder.summary()

encodop = encoder.predict(xtest)
print(encodop.shape)
prediction = model.predict(xtest)
print(prediction.shape)

n = 10
for i in range(n):
  plt.figure(figsize=(12,4))
  plt.subplot(131)
  plt.title("Original image")
  plt.imshow(xtest[i].reshape(28,28),cmap='gray')
  plt.subplot(132)
  plt.title("compressed image")
  plt.imshow(encodop[i].reshape(8,8),cmap='gray')
  plt.subplot(133)
  plt.title("Reconstructed image")
  plt.imshow(prediction[i].reshape(28,28),cmap='gray')
  plt.show()

"""## Autoencoders for denoising images"""

#load the MNIST dataset
(xtrain,ytrain),(xtest,ytest) = mnist.load_data()
#scaling the images
xtrain = (xtrain - 127.5) / 127.5
xtest = (xtest - 127.5) / 127.5
# reshaping images to channel format - samples,row,cols,channels
xtrain = xtrain.reshape(60000,28,28,1)
xtest = xtest.reshape(10000,28,28,1)
print(xtrain.shape)
print(xtest.shape)

input_layer = layers.Input(shape=(28,28,1))
c1 = layers.Conv2D(16,(3,3),activation='relu',padding='same',strides=(2,2))(input_layer)
c2 = layers.Conv2D(8,(3,3),activation='relu',padding='same',strides=(2,2))(c1)

c3 = layers.Conv2DTranspose(8,(3,3),activation='relu',padding='same',strides=(2,2))(c2)
c4 = layers.Conv2DTranspose(16,(3,3),activation='relu',padding='same',strides=(2,2))(c3)
output_layer = layers.Conv2D(1,(3,3),activation='tanh',padding='same')(c4)

model = models.Model(input_layer,output_layer)
model.summary()

from tensorflow.keras import losses
model.compile(optimizer='adam',loss=losses.MeanSquaredError())

import tensorflow as tf
noise_factor = 0.4
xtrain_noisy = xtrain + noise_factor * tf.random.normal(shape=xtrain.shape)
xtest_noisy = xtest + noise_factor * tf.random.normal(shape=xtest.shape)

xtrain_noisy = tf.clip_by_value(xtrain_noisy,-1.0,1.0)
xtest_noisy = tf.clip_by_value(xtest_noisy,-1.0,1.0)

n=10
plt.figure(figsize=(20,3))
for i in range(n):
  plt.subplot(1,n,i+1)
  plt.imshow(tf.squeeze(xtrain_noisy[i]),cmap='gray')
plt.show()

model.fit(xtrain_noisy,xtrain,epochs=20,batch_size=1000,shuffle=True,validation_data=(xtest_noisy,xtest))

prediction = model.predict(xtest_noisy)
prediction.shape

n = 10
for i in range(10):
  plt.subplot(121)
  plt.imshow(tf.squeeze(xtest_noisy[i]),cmap='gray')
  plt.subplot(122)
  plt.imshow(prediction[i].reshape(28,28),cmap='gray')
  plt.show()
