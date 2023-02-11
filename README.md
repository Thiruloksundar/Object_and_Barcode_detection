# Object and Barcode Detection

## Objective
The objective of this project is to first detect grocery items in a given background frame and then detect and decode the barcodes present in them.
The final output images contain bounding boxes according to the following criteria:
* black bounding boxes around all images with detected barcodes.
* blue bounding boxes around barcodes which were decoded.
* yellow bounding boxes around barcodes which were detected but not decoded.
* red bounding boxes around items whose barcodes weren't detected or no barcode is present. 

##Experiments
I initally approached this problem by breaking down the tasks i.e., I made three separate programs for the three different tasks. One for detecting objects,
one for detecting barcodes and the other one for decoding the barcodes.
