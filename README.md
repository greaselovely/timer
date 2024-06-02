# Countdown Timer

A simple Python application that displays a full-screen countdown timer with a black background and white numbers. When the countdown reaches zero, the screen fades to black and displays a custom message.

## Requirements

- Python 3.12 or later
- PyQt5

## Installation

1. **Install Python 3.12**:
    - Ensure you have Python 3.12 installed on your system. If not, download and install it from the [official website](https://www.python.org/downloads/).

2. **Create and activate a virtual environment**:
    ```
    python3 -m venv --system-site-packages .venv
    source .venv/bin/activate
    ```

3. **Install PyQt5**:
    ```
    pip install PyQt5
    ```

## Usage

Run the script with the starting seconds and the message as arguments:

```
python timer.py <seconds> <message>
```
