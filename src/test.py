import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QColor

class ImageDisplayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Display")
        
        # Set the fixed size of the window
        width, height = 700, 250
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
        width, height = 200, 200
        image = QImage(width, height, QImage.Format_RGB32)
        color = QColor(255, 255, 255)  # White color
        image.fill(color)
        pixmap = QPixmap.fromImage(image)
        return pixmap
    
    def choose_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose Image", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)", options=options)
        
        if file_name:
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(200, 200)  # Resize the image to 200x200
            for image_label in self.image_labels:
                image_label.setPixmap(pixmap)

def test():
    app = QApplication(sys.argv)
    window = ImageDisplayWindow()
    window.show()
    sys.exit(app.exec_())

test()