import sys
from PyQt5.QtWidgets import QMainWindow, QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import Qt

from DnC import *

class ImageDisplayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Semantic Segmentation")
        
        # Set the fixed size of the window
        # width, height = 1536, 864
        # self.setFixedSize(width, height)
        
        # Create the main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.segmentedFrame = QFrame(self)
        self.segmentedLayout = QHBoxLayout(self.segmentedFrame)
        self.segmentedLayout.setAlignment(Qt.AlignCenter)

        # Create the image labels
        self.image_labels = []
        self.captions = ["", "", ""]
        self.caption_labels = []
        for i in range(3):
            image_label = QLabel()
            image_label.setPixmap(self.get_initial_pixmap())
            if (i == 0):
                layout.addWidget(image_label,  alignment=Qt.AlignCenter)
                caption_label = QLabel(self.captions[i])
                caption_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(caption_label)
            else :
                imageFrame = QFrame()
                imageLayout = QVBoxLayout()
                imageLayout.setAlignment(Qt.AlignCenter)
                imageFrame.setLayout(imageLayout)
                imageLayout.addWidget(image_label)
                caption_label = QLabel(self.captions[i])
                caption_label.setAlignment(Qt.AlignCenter)
                imageLayout.addWidget(caption_label)
                self.segmentedLayout.addWidget(imageFrame)

            self.image_labels.append(image_label)

            self.caption_labels.append(caption_label)
        
        layout.addWidget(self.segmentedFrame)
        # Create the button to choose an image
        choose_button = QPushButton("Choose Image")
        choose_button.clicked.connect(self.choose_image)
        layout.addWidget(choose_button)
        
        # Create the central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def get_initial_pixmap(self):
        width, height = 512, 288
        image = QImage(width, height, QImage.Format_RGB32)
        color = QColor(255, 255, 255)  # White color
        image.fill(color)
        pixmap = QPixmap.fromImage(image)
        return pixmap
    
    def choose_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose Image", "", "Images (*.png *.jpg *.jpeg)", options=options)
        
        if file_name:
            result_tuple = run(file_name)
            for i in range(3):
                image_array = result_tuple[i]  # Replace with your method to load the image as a NumPy array

                height, width, channel = image_array.shape
                bytes_per_line = channel * width

                # Convert the NumPy array to a QImage
                qimage = QImage(image_array.data, width, height, bytes_per_line, QImage.Format_RGB888)

                # Convert the QImage to a QPixmap
                pixmap = QPixmap.fromImage(qimage)
                max_width, max_height = 512, 288
                pixmap = pixmap.scaled(max_width, max_height, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation) 
                self.image_labels[i].setPixmap(pixmap)
                if (i == 0):
                    self.captions[i] = "Original Image"
                elif (i == 1):
                    self.captions[i] = f"Segmented Image : R-CNN without DnC\n Number Of Objects : {result_tuple[3]} objects"
                else:
                    self.captions[i] = f"Segmented Image : R-CNN with DnC\n Number Of Objects : {result_tuple[4]} objects"
            
            for i, caption_label in enumerate(self.caption_labels):
                caption_label.setText(self.captions[i])

def run(pathfile):
    input_image = cv2.imread(pathfile)
    
    # Check if the image was successfully loaded
    if input_image is None:
        print("Failed to load image")
        exit()

    colors = np.random.randint(0, 255, (100, 3))
    
    # Threshold size for base case
    threshold_height = input_image.shape[0]//2  
    threshold_width = input_image.shape[1]//2
    dnc_segmented, dnc_count = divide_and_conquer(input_image, threshold_height, threshold_width, colors)
    without_dnc, without_dnc_count = segment_image(input_image, colors, True)

    return input_image, without_dnc, dnc_segmented, without_dnc_count, dnc_count
