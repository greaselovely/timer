import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPainter, QColor

class CountdownTimer(QWidget):
    def __init__(self, starting_seconds, message):
        super().__init__()
        self.starting_seconds = starting_seconds
        self.message = message
        self.opacity = 1.0  # Initialize opacity here
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Countdown Timer')
        self.showFullScreen()
        self.setStyleSheet("background-color: black;")

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Helvetica', 120))
        self.label.setStyleSheet("color: white;")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.update_timer()
        self.show()

    def update_timer(self):
        if self.starting_seconds >= 0:
            mins, secs = divmod(self.starting_seconds, 60)
            time_format = f"{mins:02d}:{secs:02d}"
            self.label.setText(time_format)
            self.starting_seconds -= 1
        else:
            self.timer.stop()
            self.fade_to_black()

    def fade_to_black(self):
        self.opacity = 1.0
        self.fade_timer = QTimer(self)
        self.fade_timer.timeout.connect(self.reduce_opacity)
        self.fade_timer.start(50)

    def reduce_opacity(self):
        if self.opacity > 0:
            self.opacity -= 0.05
            self.update()
        else:
            self.fade_timer.stop()
            self.show_message()

    def show_message(self):
        self.label.setText(self.message)
        self.label.setFont(QFont('Helvetica', 80))
        self.opacity = 1.0
        self.fade_in_timer = QTimer(self)
        self.fade_in_timer.timeout.connect(self.increase_opacity)
        self.fade_in_timer.start(50)

    def increase_opacity(self):
        if self.opacity < 1.0:
            self.opacity += 0.05
            self.update()
        else:
            self.fade_in_timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.setBrush(QColor(0, 0, 0))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <seconds> <message>")
        sys.exit(1)
    
    starting_seconds = int(sys.argv[1])
    message = sys.argv[2]

    app = QApplication(sys.argv)
    timer = CountdownTimer(starting_seconds, message)
    sys.exit(app.exec_())
