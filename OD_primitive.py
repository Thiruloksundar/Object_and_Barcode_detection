import cv2
image = cv2.imread('7.jpg')
edged = cv2.Canny(image, 10, 250)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
(cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in cnts:
#     peri = cv2.arcLength(c, True)
#     approx = cv2.approxPolyDP(c, peri*0.02, True)
#     cv2.drawContours(image, [approx], -1, (255,0,0), 2)
    [x,y,w,h] = cv2.boundingRect(c) 
    # discard areas that are too small 
 
    if h<40 or w<40: 
 
        continue 
    # draw rectangle around contour on original image 
 
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
cv2.imwrite('z.jpg', image)