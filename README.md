# credit-card-detection-1

detection.py is using projection to find the region of credit card in the image, and applying canny edge detection to find the contours and draw them.

findRct.py is using floodfill to divide the background and forground and using canny edge detection to find the contours. Then, using approxPolyDP fitting the contour points and try to find rectangle.
