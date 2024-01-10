#IMPORTING ALL NECESSARY MODULES
import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import matplotlib as matplotlib
import pandas as pd
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import imutils
from skimage.filters import prewitt_h,prewitt_v
from skimage.io import imread, imshow
from random import shuffle
from numpy import savetxt, asarray
from PIL import Image
from tqdm import tqdm
#DEFINING VARIABLES (might need to be changed)
TRAIN_DIR = 'D:\\AI-ML\\Data_DogVsCat\\train.dogvscat'
TEST_DIR = 'D:\\AI-ML\\Data_DogVsCat\\test.dogvscat'
IMG_SIZE = 100
LR = 1e-5
MODEL_NAME = 'dogsvscats-{}-{}.model'.format(LR, '6conv-basic')

def label_img(img):   #FUNCTION TO EXTRACT LABEL FOR EACH IMAGE
    word_label = img.split('.')[-3]  #splitting filename to extract dog/cat; example:- dog.1.jpg
    if word_label == 'cat': return [1,0]
    elif word_label == 'dog': return [0,1]

def create_train_data():  #FUNCTION TO PROCESS TRAINING DATA
    training_data = []
    for img in tqdm(os.listdir(TRAIN_DIR)):
        label = label_img(img)
        path = os.path.join(TRAIN_DIR,img)
        img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
        training_data.append([np.array(img),np.array(label)])
    shuffle(training_data)
    return training_data


def process_test_data():   #FUNCTION TO PROCESS 'FINAL' TESTING DATA
    testing_data = []
    for img in tqdm(os.listdir(TEST_DIR)):
        path = os.path.join(TEST_DIR, img)
        img_num = img.split('.')[0]
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        testing_data.append([np.array(img), np.array(img_num)])

    shuffle(testing_data)
    np.save('test_data.npy', testing_data)
    return testing_data

train_data = create_train_data() #CALLING FUNCTION TO CREATE TRAINING DATA

#\\\\\\\\\\\\\\\\ MULTILAYER PERCEPTRON DEFINITION \\\\\\\\\\\\\\\\\\\\\\\\\
tf.compat.v1.reset_default_graph()
convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 1], name='input') #INPUT LAYER

convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 128, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = fully_connected(convnet, 1024, activation='relu') #ONE FULLY CONNECTED LAYER
convnet = dropout(convnet, 0.8)

convnet = fully_connected(convnet, 2, activation='softmax') #OUTPUT LAYER, DOG/CAT
convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(convnet, tensorboard_dir='log')

if os.path.exists('{}.meta'.format(MODEL_NAME)):
    model.load(MODEL_NAME)
    print('model loaded!')

train = train_data[:-500] #SPLITTING TRAIN DATA INTO TEST/TRAIN
test = train_data[-500:]
#SPLITTING ARRAYS INTO FEATURES AND LABELS FOR BOTH TESTING AND TRAINING DATA
X = np.array([i[0] for i in train]).reshape(-1,IMG_SIZE,IMG_SIZE,1)
Y = [i[1] for i in train]
test_x = np.array([i[0] for i in test]).reshape(-1,IMG_SIZE,IMG_SIZE,1)
test_y = [i[1] for i in test]
#FITTING THE MODEL
model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),
snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

