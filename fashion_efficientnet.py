#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os, random, shutil, glob, sys

trainpath = 'data/train/'
testpath = 'data/test/'
devpath = 'data/dev/'
datapath = '/home/vudat1710/Downloads/Courses/HCSDLDPT/data_H/'

def get_random_images_from_folder(filepath, fraction):
    files = os.listdir(filepath)
    indices = list(range(0, len(files)))
    train_indices = random.sample(range(0, len(files)), int(len(files) * fraction))
    rest = list(set(indices) - set(train_indices))
    dev_indices = random.sample(rest, int(len(rest) * 0.6))
    test_indices = list(set(rest) - set(dev_indices))
    train = [files[index] for index in train_indices]
    dev = [files[index] for index in dev_indices]
    test = [files[index] for index in test_indices]

    return train, dev, test

# print(get_random_images_from_folder("/home/vudat1710/Downloads/images/data/shopee/train_images/Áo ba lỗ male/", 10))

def get_data(datapath):
    train = {}
    dev = {}
    test = {}
    
    fraction = 0.65
    
    for directory in os.listdir(datapath):
        if directory not in train.keys():
            n = len(os.listdir(datapath + directory))
            train[directory], dev[directory], test[directory] = get_random_images_from_folder(datapath + directory + '/', fraction)
    
    for key in train.keys():
        os.makedirs(trainpath + key, exist_ok=True)
        os.makedirs(testpath + key, exist_ok=True)
        os.makedirs(devpath + key, exist_ok=True)
        for fname in train[key]:
            shutil.copyfile(datapath + key + '/' + fname, trainpath + key + '/' + fname)
        for fname in test[key]:
            shutil.copyfile(datapath + key + '/' + fname, testpath + key + '/' + fname)
        for fname in dev[key]:
            shutil.copyfile(datapath + key + '/' + fname, devpath + key + '/' + fname)

get_data(datapath)


# In[15]:


for directory in os.listdir('/home/vudat1710/Downloads/images/data/shopee/train_images/'):
    n = len(os.listdir('/home/vudat1710/Downloads/images/data/shopee/train_images/' + directory))
    if n < 150:
        print (n)
        print (directory)


# In[2]:


from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=45,
    width_shift_range=0.5,
    height_shift_range=0.5,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

#hyperparams
width = 200
height = 200
input_shape = (width, height, 3)
dropout = 0.3
epochs = 30
batch_size = 32

dev_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    trainpath,
    target_size = (height, width),
    batch_size=batch_size,
    class_mode='categorical'
)

dev_generator = dev_datagen.flow_from_directory(
    devpath,
    target_size = (height, width),
    batch_size = batch_size,
    class_mode = 'categorical'
)


# In[3]:


NUM_TRAIN = 0
NUM_DEV = 0
NUM_TEST = 0
for directory in (os.listdir(trainpath)):
    NUM_TRAIN += len(os.listdir(trainpath + directory))
    NUM_TEST += len(os.listdir(testpath + directory))
    NUM_DEV += len(os.listdir(devpath + directory))

print(NUM_TRAIN, NUM_DEV)


# In[8]:


from keras.backend import sigmoid
from keras.layers import Activation
from keras.utils.generic_utils import get_custom_objects

class SwishActivation(Activation):
    
    def __init__(self, activation, **kwargs):
        super(SwishActivation, self).__init__(activation, **kwargs)
        self.__name__ = 'swish_act'

def swish_act(x, beta = 1):
    return (x * sigmoid(beta * x))

get_custom_objects().update({'swish_act': SwishActivation(swish_act)})


# In[9]:


from efficientnet.keras import EfficientNetB7
import glob
import keras
from keras.models import Model
from keras.layers import Dense, Dropout, Activation, BatchNormalization, Flatten
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam

num_classes = 25

model = EfficientNetB7(weights='imagenet', include_top=False, input_shape=input_shape, pooling='avg')
x = model.output
x = BatchNormalization()(x)
x = Dropout(dropout)(x)
x = Dense(512)(x)
x = BatchNormalization()(x)
x = Activation(swish_act)(x)
x = Dropout(dropout)(x)
x = Dense(218)(x)
x = BatchNormalization()(x)
x = Activation(swish_act)(x)

predictions = Dense(num_classes, activation="softmax")(x)
model = Model(inputs=model.input, outputs=predictions)

model.summary()


# In[ ]:


model_final.compile(loss='categorical_crossentropy',
              optimizer=Adam(0.0001),
              metrics=['accuracy'])

mcp_save = ModelCheckpoint('/gdrive/My Drive/EnetB4.h5', save_best_only=True, monitor='val_acc')
reduce_lr = ReduceLROnPlateau(monitor='val_acc', factor=0.5, patience=2, verbose=1,)

#print("Training....")
model.fit_generator(
    train_generator,
    steps_per_epoch= NUM_TRAIN //batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps= NUM_DEV //batch_size,
    verbose=1,
    use_multiprocessing=True,
    workers=1
)


test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    testpath,
    target_size = (height, width),
    batch_size=batch_size,
    class_mode='categorical'
)
_, acc = model.evaluate_generator(test_generator, NUM_TEST // batch_size, pickle_safe=False)
print("Test acc: {}%".format(acc*100))

