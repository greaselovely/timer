import os
import sys
import requests
import datetime
import argparse
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation
from PyQt5.QtGui import QFont, QPixmap

FONT_NAME = "Arial"
TIMER_FONT_SIZE = 240
MESSAGE_FONT_SIZE = 120
FADE_DURATION = 2000  # 2 SECONDS
DEFAULT_IMAGE = "background.png"
DEFAULT_SECONDS = 300  # 5 minutes
DEFAULT_MESSAGE = "And We're Back!"
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 768

class CountdownTimer(QWidget):
    def __init__(self, starting_seconds, message, background_image, full_screen, auto_start):
        super().__init__()
        self.starting_seconds = starting_seconds
        self.message = message
        self.background_image = background_image
        self.full_screen = full_screen
        self.auto_start = auto_start
        self.timer = QTimer(self)
        self.background_label = QLabel(self)  # Initialize the background_label here
        self.pixmap = QPixmap(self.background_image)  # Initialize the pixmap as an instance variable
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Countdown Timer')
        if self.full_screen:
            self.showFullScreen()
        else:
            self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
            self.show()

        self.setAutoFillBackground(False)

        # Load the background image
        if self.pixmap.isNull():
            print(f"Failed to load background image '{self.background_image}'.")
            sys.exit(1)
        self.update_background()

        # Create a timer label
        self.timer_label = QLabel(self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont(FONT_NAME, TIMER_FONT_SIZE))
        self.timer_label.setStyleSheet("color: white;")
        self.timer_opacity_effect = QGraphicsOpacityEffect()
        self.timer_opacity_effect.setOpacity(1.0)  # Set default opacity to 1.0
        self.timer_label.setGraphicsEffect(self.timer_opacity_effect)

        # Create a message label
        self.message_label = QLabel(self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFont(QFont(FONT_NAME, MESSAGE_FONT_SIZE))
        self.message_label.setStyleSheet("color: white;")
        self.message_opacity_effect = QGraphicsOpacityEffect()
        self.message_opacity_effect.setOpacity(1.0)  # Set default opacity to 1.0
        self.message_label.setGraphicsEffect(self.message_opacity_effect)
        self.message_label.hide()

        # Create a start button
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_timer)
        if auto_start: self.start_button.click()

        # Create layout and add the labels
        layout = QVBoxLayout()
        
        # Spacer to push timer_label to the center
        layout.addSpacerItem(QSpacerItem(20, 220, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)

        # Spacer to position message_label in the lower third
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.message_label, alignment=Qt.AlignCenter)

        # Spacer to ensure button is at the bottom
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.start_button, alignment=Qt.AlignRight | Qt.AlignBottom)
        
        self.setLayout(layout)

        self.update_timer()

        self.show()

    def update_background(self):
        # Scale the image while maintaining aspect ratio and fit within the window
        scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.background_label.setPixmap(scaled_pixmap)
        # Center the image
        self.background_label.setGeometry((self.width() - scaled_pixmap.width()) // 2,
                                          (self.height() - scaled_pixmap.height()) // 2,
                                          scaled_pixmap.width(),
                                          scaled_pixmap.height())

    def resizeEvent(self, event):
        # Ensure the background image scales correctly when the window is resized
        if not self.pixmap.isNull():
            self.update_background()
        super().resizeEvent(event)

    def update_timer(self):
        if self.starting_seconds >= 0:
            mins, secs = divmod(self.starting_seconds, 60)
            time_format = f"{mins:02d}:{secs:02d}"
            self.timer_label.setText(time_format)
            self.starting_seconds -= 1
        else:
            self.timer.stop()
            self.fade_out_timer()

    def start_timer(self):
        self.start_button.setDisabled(True)  # Disable the start button after starting
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def fade_out_timer(self):
        self.timer_fade_animation = QPropertyAnimation(self.timer_opacity_effect, b"opacity")
        self.timer_fade_animation.setDuration(FADE_DURATION)
        self.timer_fade_animation.setStartValue(1)
        self.timer_fade_animation.setEndValue(0)
        self.timer_fade_animation.finished.connect(self.show_message)
        self.timer_fade_animation.start()

    def show_message(self):
        self.message_label.setText(self.message)
        self.message_label.show()
        self.fade_in_message()

    def fade_in_message(self):
        self.message_opacity_effect.setOpacity(0)
        self.message_fade_animation = QPropertyAnimation(self.message_opacity_effect, b"opacity")
        self.message_fade_animation.setDuration(FADE_DURATION)
        self.message_fade_animation.setStartValue(0)
        self.message_fade_animation.setEndValue(1)
        self.message_fade_animation.start()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Countdown Timer')
    parser.add_argument('-i', '--image', type=str, default=DEFAULT_IMAGE, help=f'Path to the background image file (default: {DEFAULT_IMAGE})')
    parser.add_argument('-s', '--sec', type=int, default=DEFAULT_SECONDS, help=f'Number of seconds for the countdown (default: {DEFAULT_SECONDS})')
    parser.add_argument('-m', '--message', type=str, default=DEFAULT_MESSAGE, help=f'Message to display after the countdown (default: {DEFAULT_MESSAGE})')
    parser.add_argument('-f', '--fullscreen', action='store_true', help='Run the timer in full-screen mode')
    parser.add_argument('-a', '--auto_start', action='store_true', help='Auto Start the Timer')
    
    return parser.parse_args()

def get_online_image(url):
    home_dir = os.path.expanduser('~')
    image = requests.get(url, verify=False)
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = os.path.join(home_dir, f'image_{timestamp}.jpg')
    if not image: 
        print("Not a valid image")
        sys.exit(1)
    with open(filename, 'wb') as f:
        f.write(image.content)
    return filename 


if __name__ == '__main__':
    args = parse_arguments()

    starting_seconds = args.sec
    message = args.message
    background_image = args.image
    if background_image.startswith('http'):
        background_image = get_online_image(background_image)
    full_screen = args.fullscreen
    auto_start = args.auto_start

    app = QApplication(sys.argv)
    timer = CountdownTimer(starting_seconds, message, background_image, full_screen, auto_start)  # Start a countdown with the provided arguments
    sys.exit(app.exec_())
