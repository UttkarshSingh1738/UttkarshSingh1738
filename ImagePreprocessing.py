import matplotlib as matplotlib
import pandas as pd
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import imutils
from skimage.filters import prewitt_h,prewitt_v
from skimage.io import imread, imshow
from numpy import savetxt
from PIL import Image
from tqdm import tqdm
img_size = 50
directory = "D:\AI-ML"
for filename in tqdm(os.listdir(directory)):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        Image_Path = (os.path.join(directory, filename))
        orignal_img = imread(Image_Path)
        plt.imshow(orignal_img)
        plt.show()
        orignal_img = imread(Image_Path, as_gray=True)
        img = imutils.resize(cv2.imread(Image_Path, cv2.IMREAD_GRAYSCALE), height=img_size)
        edges_prewitt_horizontal = prewitt_h(img)
        edges_prewitt_vertical = prewitt_v(img)
        print(edges_prewitt_vertical)
        print(edges_prewitt_horizontal)
        gradient = np.sqrt((edges_prewitt_horizontal)**2+(edges_prewitt_vertical)**2)
        sharpened = gradient+img
        plt.imshow(edges_prewitt_horizontal, cmap='gray')
        plt.show()
        plt.imshow(edges_prewitt_vertical, cmap='gray')
        plt.show()
        plt.imshow(sharpened, cmap='gray')
        plt.show()

