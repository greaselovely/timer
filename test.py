import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap

class ImageTest(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Test')
        self.showFullScreen()

        # Load the image
        self.background_label = QLabel(self)
        self.pixmap = QPixmap(self.image_path)
        if self.pixmap.isNull():
            print(f"Failed to load image '{self.image_path}'")
            sys.exit(1)
        self.background_label.setPixmap(self.pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(self.rect())

        layout = QVBoxLayout()
        layout.addWidget(self.background_label)
        self.setLayout(layout)
        self.show()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]

    app = QApplication(sys.argv)
    test = ImageTest(image_path)
    sys.exit(app.exec_())
