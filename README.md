# Countdown Timer

This Python script creates a countdown timer with a background image and a message display after the timer ends. It uses PyQt5 for the graphical user interface.

## Features

- Full-screen countdown timer.
- Customizable background image.
- Timer and message font customization.
- Fade-out effect for the timer and fade-in effect for the message.
- Default values for background image, countdown duration, and message.

## Requirements

- Python 3.x
- PyQt5

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/greaselovely/timer
   cd timer
   ```

2. **Create a virtual environment:**

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install PyQt5
   ```

## Usage

You can run the script with optional arguments for the background image, countdown duration, and message. If no arguments are provided, default values will be used.

### Command-line Arguments

- `-i` or `--image`: Path to the background image file (default: `background.png`)
- `-s` or `--sec`: Number of seconds for the countdown (default: `300` seconds or 5 minutes)
- `-m` or `--message`: Message to display after the countdown (default: `"And We're Back!"`)

### Running the Script

Run the script with default values:

```sh
python timer.py
```

Run the script with custom values:

```sh
python timer.py -i custom_background.png -s 600 -m "Break Time Over!"
```

## Example

```sh
python timer.py -i background.png -s 300 -m "And We're Back!"
```

This command will start a countdown timer for 5 minutes with `background.png` as the background image and display the message `"And We're Back!"` after the timer ends.

## Script Details

### Constants

- `FONT_NAME`: Font name for the timer and message (default: `Arial`)
- `TIMER_FONT_SIZE`: Font size for the timer (default: `240`)
- `MESSAGE_FONT_SIZE`: Font size for the message (default: `120`)
- `FADE_DURATION`: Duration of the fade effects in milliseconds (default: `2000` ms)
- `DEFAULT_IMAGE`: Default background image file (default: `background.png`)
- `DEFAULT_SECONDS`: Default countdown duration in seconds (default: `300` seconds or 5 minutes)
- `DEFAULT_MESSAGE`: Default message to display after the countdown (default: `"And We're Back!"`)

### Classes and Functions

- `CountdownTimer`: Main class for the countdown timer window.
- `initUI()`: Initializes the user interface.
- `update_background()`: Updates the background image.
- `resizeEvent(event)`: Handles window resize events.
- `update_timer()`: Updates the timer display.
- `fade_out_timer()`: Handles the fade-out effect for the timer.
- `show_message()`: Displays the message after the timer ends.
- `fade_in_message()`: Handles the fade-in effect for the message.
- `parse_arguments()`: Parses command-line arguments using `argparse`.
