# Object and Barcode Detection

## Objective
The objective of this project is to first detect grocery items in a given background frame and then detect and decode the barcodes present in them.
The final output images contain bounding boxes according to the following criteria:
* black bounding boxes around all images with detected barcodes.
* blue bounding boxes around barcodes which were decoded.
* yellow bounding boxes around barcodes which were detected but not decoded.
* red bounding boxes around items whose barcodes weren't detected or no barcode is present. 

## Experiments and Results
I initally approached this problem by breaking down the tasks i.e., I made three separate programs for the three different tasks. One for detecting objects, one for detecting barcodes and the other one for decoding the barcodes.
The first code I wrote for item detection was OD_primitive. In this, I just used contour detection to find and draw bounding boxes around items present in the image.
The accuracy of this implementation was poor and it also detected some unwanted parts in the item along with it. Sometimes, it didnt identify the item completely. As an example, the input image I gave was

![7](https://user-images.githubusercontent.com/95955774/218242805-d3472ebe-ce55-4472-8743-cb358cdc73bb.jpg)

and the output was

![z](https://user-images.githubusercontent.com/95955774/218242833-9d6e6ade-d3d1-47f4-9c97-814726af3310.jpg)

Similarly, the barcode detector and decoders' results were not that good.
The detector detected other letters and words in the items too as barcodes. 
For example,
![k](https://user-images.githubusercontent.com/95955774/218243083-d0615205-4711-4b48-8487-4c8a62fb6b88.jpg)

but some results were good
![s](https://user-images.githubusercontent.com/95955774/218243105-d4e3d760-c5a3-4a1b-9f8b-1278a5b89e5b.jpg)

The detector I used was the pyzbar barcode detector. It didn't detect all the item barcodes when many items were present,
![h](https://user-images.githubusercontent.com/95955774/218243319-f8b210ad-0964-443e-aa2c-6c711701954b.jpg)

The barcode detectors' results weren't upto the mark since I had sent the whole input image as an input to the detector. It would have given better results if I had cropped out the detected image and then sent it as input to the detector. For this, the object detector must be highly accurate and detect all objects completely.

So, my next idea was to try pretrained deep learning vision models to detect the objects in the image. I tried pretrained yolov4 and yolov7 models.
I ran these models using the darknet framework which I had setup in my device previously. To try your own vision models setup darknet, open command prompt and move to the darknet directory and add your model weights in the cfg folder and test images in the data folder. Then execute
```
C:/Users/darknet> darknet.exe detect cfg/yolov4.cfg cfg/yolov4.weights #(your weights) data/4.jpg #(your image)
```
The result of the pretrained yolov4 model was 
![2023-02-11](https://user-images.githubusercontent.com/95955774/218243798-1cd0e1ce-8433-4a9f-a7bb-0adde095a781.png)

It didn't give good results since the model wasn't finetuned for grocery item detection. I didn't try finetuning deep learning models due to high gpu requirements.

## Current Implementation
Finally, I decided to use HSV segementation and Canny edge detection techniques to detect items in the image and send the cropped items as an input to the barcode scanner. I used OpenCV's inbuilt barcode detector and decoder this time since it is easier to implement and has a good accuracy. To run the final implementation you can clone my repo and run the final.py or add the HSV_contours.py, utils and final.py codes to your working directory and execute it on your machine.
The final results are
![r_4](https://user-images.githubusercontent.com/95955774/218244291-dfb9f344-184b-4835-a826-ddd149100a47.jpg)

![r_12](https://user-images.githubusercontent.com/95955774/218244318-71fa8844-04d5-474a-9241-de029e7e80a6.jpg)
The other results can be found in the final results folder.

## Further Ideas
The ideas I have in mind to improve the detector is to try and train a deep learning detection model on a grocery items dataset and use it instead of the HSV and Canny edge detection method to find the items in the frame. Improving the detector would directly improve the results since the cropped part identified by the detector is sent as an input to the barcode decoder. 
Feel free to suggest any other methods or ideas you might have to improve my project.
