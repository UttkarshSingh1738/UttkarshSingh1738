import cv2

# reading image
image = cv2.imread('D:\AI-ML\Data-Resolute-AI-Internship\\task_2.jpg')
scale_percent = 20 # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
# thresholding the image
ret,thresh = cv2.threshold(image, 10*10, 255, cv2.THRESH_BINARY_INV)
edged = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
cv2.imshow('check', edged)

contours,h = cv2.findContours(edged, cv2.RETR_TREE,
                    cv2.CHAIN_APPROX_SIMPLE)
#cv2.imshow('img', thresh)

# looping through contours
num =0
for cnt in contours:

    x, y, w, h = cv2.boundingRect(cnt)
    if w > 50 and h > 50:

        #ADDED SIZE CRITERION TO REMOVE NOISES
        size = cv2.contourArea(cnt)
        if size > 500:
            num =num + 1
            #CHANGED DRAWING CONTOURS WITH RECTANGLE
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,215,255),2)

print (num)
cv2.imshow('img', image)
cv2.waitKey(0)
cv2.destroyAllWindows()