import cv2
import numpy as np

def getColor(colors, i):
    return  (int(colors[i][0]), int(colors[i][1]), int(colors[i][2]))


def segment_image(image, colors, giveBox):
    count = 0

    # Loading mask RCNN model
    mask_rcnn = cv2.dnn.readNetFromTensorflow("src/dnn/frozen_inference_graph_coco.pb", "src/dnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")

    if (len(image.shape) == 2):
        h, w = image.shape
    else : 
        h, w, _ = image.shape

    # background image
    baseImage = np.zeros((h, w, 3), np.uint8)
    baseImage[:] = getColor(colors, 99)

    # detect objects in the image
    blob = cv2.dnn.blobFromImage(image, swapRB=True)
    mask_rcnn.setInput(blob)

    # Run the Mask R-CNN model to obtain potential object masks
    boxes, masks = mask_rcnn.forward(["detection_out_final", "detection_masks"])
    detection_count = boxes.shape[2] # maximum 100 objects

    for i in range(detection_count):

        box = boxes[0, 0, i]
        class_id = box[1]
        # print("class id: ",class_id)
        score = box[2]
        # print("score: ",score)
        if score==0.0:
            continue

        x = int(box[3]* w)
        y = int(box[4]* h)
        x1 = int(box[5]* w)
        y1 = int(box[6]* h)

        roi = baseImage[y:y1, x:x1]
        roiHeight, roiWidth, _ = roi.shape

        mask = masks[i, int(class_id)]
        mask = cv2.resize(mask, (roiWidth, roiHeight))
        _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)
        # print(mask)

        if giveBox:
            cv2.rectangle(image, (x, y), (x1, y1), (0, 255, 0), 3)
        
        count+=1

        # Get mask dimensions
        contours, _ = cv2.findContours(np.array(mask, np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        color = colors[int(class_id)]
        for cnt in contours:
            cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))
    
    return baseImage, count
