import cv2
import numpy as np
from pathlib import Path
import glob
import matplotlib.pyplot as plt
from utils.general import draw_bbox_barcode
from HSV_Contours import hsv_seg, contours

red = (255,0,0)
blue = (0,0,255)
yellow = (255, 255,0)

def run(image_path, bardet, draw_all_objects=False):

    contlist , boxes, _, orig= contours(image_path)
    orig = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)

    result = np.copy(orig)
    if not len(boxes):
        print('Did not find any items\n')
    else:
        total_barcodes = {}
        for idx, box in enumerate(boxes):
            # Crop Object detected
            x1,y1,w,h = box
            x2, y2 = x1+w, y1+h
            item = orig[y1:y2,x1:x2,:].copy()
            if 0 in item.shape:
                continue

            item = cv2.cvtColor(item, cv2.COLOR_RGB2BGR)
            found, decoded_info, decoded_type, detections = bardet.detectAndDecode(item)
            if draw_all_objects:
                cnt = contlist[idx]
                area = cv2.contourArea(cnt)
                hull = cv2.convexHull(cnt)
                hullarea = cv2.contourArea(hull)
                if hullarea/area > 1.3:
                    cv2.putText(result, 'Multiple Objects', (x1,y1), cv2.FONT_HERSHEY_SIMPLEX,5, (255,255,255), 10, cv2.LINE_AA)

                result = cv2.rectangle(result, (x1,y1), (x2,y2), red, 20)
                
            # Checking barcodes detected by OpenCV
            if detections is None:
                # Red Bbox around object with no barcode
                result = cv2.rectangle(result, (x1,y1), (x2,y2), red, 20)
                
            else:
                detections = np.round_(detections).astype(np.uint16)
                for i in range(detections.shape[0]):
                    y = total_barcodes.get(decoded_info[i])
                    if decoded_info[i] == '':
                        # Barcode detected But Not decoded
                        # draw Bbox for barcode
                        corners = detections[i]
                        orig_corners = corners.copy()
                        orig_corners[:,0]+=x1
                        orig_corners[:,1]+=y1
                        result = draw_bbox_barcode(result, orig_corners, yellow)
                        
                    # check if barcode is already found
                    elif total_barcodes.get(decoded_info[i]) is not None:   
                        total_barcodes[decoded_info[i]]+=1
                        # draw Bbox for barcode
                        corners = detections[i].copy()
                        corners[:,0]+=x1
                        corners[:,1]+=y1
                        result = draw_bbox_barcode(result, corners, blue)
                        
                    else:
                        # Found a new Barcode
                        # draw Bbox for barcode
                        total_barcodes[decoded_info[i]]=1
                        corners = detections[i].copy()
                        corners[:,0]+=x1
                        corners[:,1]+=y1
                        result = draw_bbox_barcode(result, corners, blue)
        
        if len(total_barcodes):
            print('Item code     |  Count of Item')
            for item_code, count in total_barcodes.items():
                print(item_code,count,sep='    |  ')
            print('\n')
        else:
            print('Could not find any barcodes\n')
#     print(total_barcodes)
    return orig, result

if __name__=='__main__':
    
    # folder path
    folder_path = 'C:/Users/Thirulok Sundar/barcode'
    images = glob.glob(folder_path.__str__()+'/*.jpg')

    # Initialize Barcode Detector
    bardet = cv2.barcode_BarcodeDetector()
    if not len(images):
        print('No image folder specified')
    i=0
    for image in images:
        i+=1
        orig, result =  run(image, bardet, True)
        plt.imshow(result)
        k = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        cv2.imwrite('r_{i:}.jpg'.format(i=i), k)
        plt.show()