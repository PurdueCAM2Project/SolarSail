# -*- coding: utf-8 -*-
"""New_Blur_Classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ry-lmalg6hZdBTOizjGN_D6jWJ-ZGJsA
"""

!pip uninstall tensorflow-addons
!pip install tensorflow-addons
import tensorflow_addons as tfa
import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import tensorflow.keras as ks

ds, info = tfds.load('beans', split = 'train', as_supervised=True, with_info = True)
size = info.splits['train'].num_examples
ds = ds.batch(1)

def preprocess_norm(image, label):
    image = tf.cast(image, tf.float32)
    image = image / 255.
    image = tf.image.sobel_edges(image)
    image = tf.math.square(image)
    image = tf.reduce_sum(image, axis = -1)
    image = tf.sqrt(image)
    image = tf.image.resize(
    image, [300, 300], preserve_aspect_ratio=False,
    antialias=False, name=None)
    label = tf.constant([[0]], dtype = tf.float32)
    return image, label

def preprocess_gaus(image, label):
  image = tf.cast(image, tf.float32)
  image = tfa.image.gaussian_filter2d(image=image,
                                      sigma = 100,
                                      filter_shape=[5, 5])

  image = tf.image.sobel_edges(image)
  image = tf.math.square(image)
  image = tf.reduce_sum(image, axis = -1)
  image = tf.sqrt(image)

  image = image / 255
  image = tf.image.resize(
    image, [300, 300], preserve_aspect_ratio=False,
    antialias=False, name=None)
  label = tf.constant([[1]], dtype = tf.float32)

  return image, label

norm = ds.take(size // 2)
gaus = ds.skip(size // 2).take(size // 2)
norm = norm.map(preprocess_norm)
gaus = gaus.map(preprocess_gaus)

train = norm.concatenate(gaus)
print(train)

train = train.shuffle(size)
train = train.prefetch(tf.data.experimental.AUTOTUNE)

for img, label in train.take(1):
    print(label.shape)
    break

model = ks.Sequential()
model.add(ks.layers.Conv2D(7, kernel_size = (3,3), strides = (2,2), padding = "same"))# inital feature extraction, get the most important information, so less filters is better, do a single down sample
model.add(ks.layers.Activation(activation = "relu"))
model.add(ks.layers.Conv2D(64, kernel_size = (3,3), strides = (1,1), padding = "same"))
model.add(ks.layers.Activation(activation = "relu"))
model.add(ks.layers.Conv2D(64, kernel_size = (3,3), strides = (1,1), padding = "same"))
model.add(ks.layers.Activation(activation = "relu"))
model.add(ks.layers.Conv2D(32, kernel_size = (3,3), strides = (2,2), padding = "same"))
model.add(ks.layers.Activation(activation = "relu"))
model.add(ks.layers.Conv2D(16, kernel_size = (3,3), strides = (2,2), padding = "same"))
model.add(ks.layers.Activation(activation = "relu"))
model.add(ks.layers.Conv2D(2, kernel_size = (3,3), strides = (2,2), padding = "same"))
model.add(ks.layers.Activation(activation = "relu"))
model.add(ks.layers.GlobalAvgPool2D())
model.add(ks.layers.Activation(activation = "relu"))
model.add(ks.layers.Dense(2))
model.add(ks.layers.Activation(activation = "softmax"))

model.compile(optimizer= 'adam', loss = tf.keras.losses.SparseCategoricalCrossentropy(), metrics = ['accuracy'])
model.fit(train, epochs=10)

model.summary()