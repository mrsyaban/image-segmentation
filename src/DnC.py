import numpy as np
import cv2
import matplotlib.pyplot as plt

from RCNN_segmentation import segment_image

def divide_and_conquer(image, threshold_height, threshold_width, colors):
    
    count = 0

    # Base
    if image.shape[0] <= threshold_height and image.shape[1] <= threshold_width:
        return image

    # Rekurens
    else :
        # Divide the image into smaller subregions
        subregions = divide_image(image)

        segmented_regions = []
        for subregion in subregions:
            # Apply a R-CNN Algorithm to each subregion
            segmented_subregion, temp_count = segment_image(subregion, colors, False)
            count += temp_count
            # Recursively segment each subregion if necessary
            if segmented_subregion.shape[0] > threshold_height and segmented_subregion.shape[1] > threshold_width:
                segmented_subregion = divide_and_conquer(segmented_subregion, threshold_height, threshold_width)

            segmented_regions.append(segmented_subregion)

        # Combine the segmented subregions
        combined_image = combine_images(segmented_regions)

        return combined_image, count

def divide_image(image):
    # Divide the image into quadrants
    height, width = image.shape[:2]
    half_height = height // 2
    half_width = width // 2

    subregion1 = image[:half_height, :half_width]
    subregion2 = image[:half_height, half_width:]
    subregion3 = image[half_height:, :half_width]
    subregion4 = image[half_height:, half_width:]

    return [subregion1, subregion2, subregion3, subregion4]

def combine_images(images):
    # Combine the segmented subregions 
    combined_image = np.vstack((np.hstack((images[0], images[1])), np.hstack((images[2], images[3]))))

    return combined_image

