import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import Qt

from DnC import *

class ImageDisplayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Display")
        
        # Set the fixed size of the window
        width, height = 1536, 864
        self.setFixedSize(width, height)
        
        # Create the main layout
        layout = QHBoxLayout()
        
        # Create the image labels
        self.image_labels = []
        for _ in range(3):
            image_label = QLabel()
            image_label.setPixmap(self.get_initial_pixmap())
            layout.addWidget(image_label)
            self.image_labels.append(image_label)
        
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

    return input_image, dnc_segmented, without_dnc, dnc_count,  without_dnc_count

    # fig, axs = plt.subplots(1, 3, figsize=(12, 4))

    # axs[0].imshow(input_image)
    # axs[1].imshow(dnc_segmented)
    # axs[2].imshow(without_dnc)

    # for ax in axs:
    #     ax.axis('off')

    # axs[0].set_title('Original Image', fontsize=12, weight='bold')
    # axs[1].set_title('DnC Segmented Image', fontsize=12, weight='bold')
    # axs[2].set_title('Without DnC Segmented Image', fontsize=12, weight='bold')

    # axs[0].text(0.5, -0.15, 'Original Image', transform=axs[0].transAxes, ha='center', fontsize=12, weight='bold')
    # axs[2].text(0.5, -0.15, f'Jumlah Objek: {without_dnc_count}', transform=axs[2].transAxes, ha='center', fontsize=12, weight='bold')
    # axs[1].text(0.5, -0.15, f'Jumlah Objek: {dnc_count}', transform=axs[1].transAxes, ha='center', fontsize=12, weight='bold')

    # plt.tight_layout(pad=2)
    # plt.show()

