import cv2
import numpy as np
from skimage.io import imread, imshow
from matplotlib import pyplot as plt
image_path = 'D:\\AI-ML\\Data_BoxDetection\\uenUq.png'
image = cv2.imread(image_path)
scale_percent = 100 # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
cv2.imshow('image', image)
gray = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLOR_BGR2RGB)
blur = cv2.medianBlur(gray, 5)
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

thresh = cv2.threshold(sharpen,160,255, cv2.THRESH_BINARY_INV)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
close = cv2.cvtColor(close, cv2.COLOR_BGR2GRAY);
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

min_area = 150
max_area = 3000
image_number = 0
for c in cnts:
    area = cv2.contourArea(c)
    if area > min_area and area < max_area:
        x,y,w,h = cv2.boundingRect(c)
        ROI = image[y:y+h, x:x+h]
        cv2.imwrite('D:\\AI-ML\\Data_Boxdetection\\ROI_{}.png'.format(image_number), ROI)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
        image_number += 1
print(image_number)
#cv2.imshow('sharpen', sharpen)
#cv2.imshow('close', close)
#cv2.imshow('thresh', thresh)
#cv2.imshow('image', image)
cv2.waitKey()