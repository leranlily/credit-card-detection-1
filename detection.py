#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
MAX_WIDTH = 1000
height = 5.5
width = 8.5
ratio = width/height

img = cv2.imread("3.jpg")
h, w, channels = img.shape
if w > MAX_WIDTH:
	resize_rate = MAX_WIDTH / w
	img = cv2.resize(img, (MAX_WIDTH, int(h*resize_rate)), interpolation=cv2.INTER_AREA)
h, w, channels = img.shape
edge = w//100

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3,3), 0)   # gaussian filtering
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  #binary
judge = 0
if binary[0,0]==255:
    judge = judge + 1
if binary[0,w-1]==255:
    judge = judge + 1
if binary[h-1,0]==255:
    judge = judge + 1
if binary[h-1,w-1]==255:
    judge = judge + 1
if judge>=3:
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Projection
up = 0
down = h
left = 0
right = w
maxh = 0
maxw = 0
threshold = 0.4
hsum = np.sum(binary,axis=1)  # sum of each row

for y in range (0,h):
    if (hsum[y]>maxh):
        maxh = hsum[y]


for y in range(h-1, 0,-1):
    if (hsum[y])>maxh*threshold:
        down = y
        break
    
for y in range(0, h):
    if (hsum[y])>maxh*threshold:
        up = y
        break

wsum = np.sum(binary[up:down,:],axis=0) #sum of each column

for x in range (0,w):
    if (wsum[x]>maxw):
        maxw = wsum[x]

for x in range(0, w):
    if (wsum[x]>maxw*threshold):
        left = x
        break
        
for x in range(w-1, 0, -1):
    if (wsum[x]>maxw*threshold):
        right = x
        break

right = min(w-1,right+edge)
left = max(0,left-edge)
up = max(0,up-edge)
down = min(h-1,down+edge)
        
r = (right-left)/(down-up)
if r<1.2:
    neww = int((down-up)*ratio)
    addw = neww - (right-left)
    if neww >= w:
        right = w-1
        left = 0
    else:
        if (right+addw//2<w):
            if (left-addw//2>0):
                right = right+addw//2
                left = left-addw//2
            else:
                left = 0
                right = addw
        else:
            right = w-1
            left = w - addw
elif r>1.9:
    newh = int((right-left)//ratio)
    addh = newh-(down-up)
    if newh >= h:
        up = 0
        down = h-1
    else:
        if (down+addh//2<h):
            if (up-addh//2>0):
                down = down+addh//2
                up = up-addh//2
            else:
                up = 0
                down = addh
        else:
            down = h-1
            up = h - addh


dst = gray[up:down, left:right] 
img_dst = cv2.Canny(dst, 100, 200)
image, contours, hierarchy = cv2.findContours(img_dst,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
cv2.drawContours(img[up:down, left:right],contours,-1,(0,0,255),1)  
cv2.imwrite("dst3.jpg",dst)   
cv2.imshow("result", img)
cv2.imshow("1", binary)
cv2.imshow("2", dst)

cv2.waitKey(0)  
cv2.destroyAllWindows()
