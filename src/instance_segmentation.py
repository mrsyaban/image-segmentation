import cv2
import numpy as np

# Loading mask RCNN model
mask_rcnn = cv2.dnn.readNetFromTensorflow("src/dnn/frozen_inference_graph_coco.pb", "src/dnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")

colors = np.random.randint(0, 255, (100, 3))


# Load the image
image = cv2.imread("test/bedroom.jpg")
h, w, _ = image.shape

# background image
background = np.zeros((h, w, 3), np.uint8)
background[:] = (int(colors[81][0]), int(colors[81][1]), int(colors[81][2]))  # (B, G, R)

# Check if the image was successfully loaded
if image is None:
    print("Failed to load image")
    exit()

# detect objects in the image
blob = cv2.dnn.blobFromImage(image, swapRB=True)
mask_rcnn.setInput(blob)

# Run the Mask R-CNN model to obtain potential object masks
boxes, masks = mask_rcnn.forward(["detection_out_final", "detection_masks"])
detection_count = boxes.shape[2] # maximum 100 objects

print("Found %d objects in the image." % detection_count)

count = 0

for i in range(detection_count):

    box = boxes[0, 0, i]
    class_id = box[1]
    print("class id: ",class_id)
    score = box[2]
    print("score: ",score)
    if score==0.0:
        continue

    x = int(box[3]* w)
    y = int(box[4]* h)
    x1 = int(box[5]* w)
    y1 = int(box[6]* h)

    roi = background[y:y1, x:x1]
    roiHeight, roiWidth, _ = roi.shape

    mask = masks[i, int(class_id)]
    mask = cv2.resize(mask, (roiWidth, roiHeight))
    _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)
    # print(mask)

    cv2.rectangle(image, (x, y), (x1, y1), (0, 255, 0), 3)
    count+=1

    # Get mask dimensions
    contours, _ = cv2.findContours(np.array(mask, np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    color = colors[int(class_id)]
    for cnt in contours:
        # hull = cv2.convexHull(cnt)
        cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))

    # cv2.imshow("Mask", mask)
    # cv2.imshow("roi", roi)
    # cv2.waitKey(0)

# Resize the image window
window_width = image.shape[1]
window_height = image.shape[0]
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image', window_width, window_height)
cv2.namedWindow('Background', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Background', window_width, window_height)


print(count)
cv2.imshow("Image", image)
cv2.imshow("Background", background)
cv2.waitKey(0)