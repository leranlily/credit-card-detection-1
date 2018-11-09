import cv2
import numpy as np
import math

MAX_WIDTH = 1000
height = 5.5
width = 8.5
ratio = width/height

#calculate the angle of three points
def angle(d1,d2,d3):
    x1,y1,x2,y2,x3,y3 = d1[0,0],d1[0,1],d2[0,0],d2[0,1],d3[0,0],d3[0,1]
    
    a=math.sqrt((x2-x3)*(x2-x3)+(y2-y3)*(y2-y3))
    b=math.sqrt((x1-x3)*(x1-x3)+(y1-y3)*(y1-y3))
    c=math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
    B=math.degrees(math.acos((b*b-a*a-c*c)/(-2*a*c)))
    return a, c, B

#calculate the forth point with three points in rectangle
def point4(d1,d2,d3):
    x1,y1,x2,y2,x3,y3 = d1[0,0],d1[0,1],d2[0,0],d2[0,1],d3[0,0],d3[0,1]
    x4 = x1+x3-x2
    y4 = y1+y3-y2
    d4 = [[x4,y4]]
    return d4

img = cv2.imread("1.jpg")
img = cv2.GaussianBlur(img,(3,3),0)  # gaussian filtering

h, w = img.shape[:2]
if w > MAX_WIDTH:
	resize_rate = MAX_WIDTH / w
	img = cv2.resize(img, (MAX_WIDTH, int(h*resize_rate)), interpolation=cv2.INTER_AREA)
h, w, channels = img.shape
MIN_AREA = h*w/100

#floodfill
blured = cv2.blur(img,(5,5))
mask = np.zeros((h+2, w+2), np.uint8)
cv2.floodFill(blured, mask, (w-1,h-1), (255,255,255), (2,2,2),(3,3,3),8)
gray = cv2.cvtColor(blured,cv2.COLOR_BGR2GRAY)  

#openning and closing
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(50, 50))
opened = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)  
closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)  

#canny detect edge
img_edge = cv2.Canny(closed, 50, 150)

image, contours, hierarchy = cv2.findContours(img_edge,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)   

#find rectangle in contours
for i in range(length):
    cnt = contours[i]
    epsilon = 0.02 * cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    if len(approx)>=3:
        for k in range(0,len(approx)-1):
            a, c, B = angle(approx[k],approx[(k+1)%len(approx)],approx[(k+2)%len(approx)])
            if B<95 and B>90 :
                print(a,c,B)
                w1 = max(a,c)
                h1 = min(a,c)
                if w1/h1<1.8 and w1/h1> 1.4:
                    d4 = point4(approx[k],approx[(k+1)%len(approx)],approx[(k+2)%len(approx)])
                    cv2.polylines(img, [np.array([approx[k],approx[(k+1)%len(approx)],approx[(k+2)%len(approx)],d4],np.int32)], True, (0, 0, 255), 1)
                    break


cv2.imshow("approx",img)
cv2.waitKey(0)
cv2.destroyAllWindows() 
