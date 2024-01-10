import cv2
import numpy as np
import imutils
import pytesseract
import tqdm
import os
import easyocr
from matplotlib import pyplot as plt
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'D:/Tesseract-OCR/tesseract.exe'
directory = "Provide Data Directory Path"
for filename in os.listdir(directory):
    if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".JPG"):
        Image_Path = (os.path.join(directory, filename))
        img = cv2.imread(Image_Path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
        #plt.show()
        bfilter = cv2.bilateralFilter(gray, 11, 15, 19)
        edged = cv2.Canny(bfilter, 50, 200)
        #plt.show()
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
        # print(location)
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)
        plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
        #plt.show()
        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2 + 1, y1:y2 + 1]
        plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        # plt.show()
        # text = pytesseract.image_to_string(cropped_image)
        # print(text)
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        # print(result)
        text = result[0][-2]
        #print(text)
        font = cv2.FONT_ITALIC
        res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1] + 60), fontFace=font, fontScale=1,
                          color=(255, 0, 255), thickness=4, lineType=cv2.LINE_4)
        res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0, 255, 0), 3)
        plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
        plt.show();
