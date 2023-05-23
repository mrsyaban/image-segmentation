from PyQt5.QtWidgets import QApplication
from utility import *

def main():
    app = QApplication(sys.argv)
    window = ImageDisplayWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()