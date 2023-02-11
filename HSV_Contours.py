import cv2
import numpy as np

def hsv_seg(orig):
    """HSV + Edge Segmentation for white background removal. Returns Foreground mask."""
    
    img = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # hsv mask
    mask = cv2.inRange(img, (0,0,100), (179,100,255)) # hsv mask with white background
    mask = cv2.bitwise_not(mask) # mask to remove background

    # edge 
    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray,100,255)
    
    # Dilate edges
    dilatation_size = 25
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (2 * dilatation_size + 1, 2 * dilatation_size + 1),(-1, -1))
    diledge = cv2.dilate(edges, element) 
    
    # Sum of HSV and dilated Edges
    summed = diledge + mask 
    dilatemask = cv2.dilate(summed, element)
    
    # eroded
    ero = cv2.erode(dilatemask, element, iterations=2)

    
    # Specify size on horizontal axis
    cols = orig.shape[1]
    horizontal_size = cols // 30
    horizontal = ero
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 20))
    # Apply morphology operations
    horizontal = cv2.morphologyEx(horizontal,cv2.MORPH_OPEN, horizontalStructure, iterations=2)

    # Specify size on vertical axis
    rows = orig.shape[0]
    vertical_size = rows // 30
    vertical = ero
    # Create structure element for extracting horizontal lines through morphology operations
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (20,vertical_size))
    # Apply morphology operations
    vertical = cv2.morphologyEx(vertical,cv2.MORPH_OPEN, verticalStructure, iterations=2)
    
    nmask = cv2.bitwise_and(horizontal, vertical)
    
    # Close image to remove holes in objects
    dilatation_size = 25
    element = cv2.getStructuringElement(cv2.MORPH_RECT, ( dilatation_size + 1, dilatation_size + 1),(-1, -1))
    
    nmask = cv2.morphologyEx(nmask, cv2.MORPH_CLOSE, element, iterations=2)
    
    return nmask

def contours(path):
    orig = cv2.imread(path)
    img = np.copy(orig)
    fgmask = hsv_seg(img)
  
    # Contours in Foreground mask
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    imgcont = cv2.drawContours(np.copy(orig), contours, -1, (255,0,0), 10)
    contlist=[]
    boxes = []
    for i,cnt in enumerate(contours):
        x,y,w,h = cv2.boundingRect(cnt)
        if w>100 and h>100:
            if (w>h and w//h<5) or (h>=w and h//w < 5):
                contlist.append(cnt)
                boxes.append([x,y,w,h])
                cv2.rectangle(imgcont,(x,y),(x+w,y+h),(0,255,0),20)
                cv2.putText(imgcont, str(i), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 
                           5, (255,0,255), 10, cv2.LINE_AA)
    boxes = np.array(boxes)
    return contlist,boxes, imgcont, orig