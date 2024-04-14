# Face Detection and Targeting System

This Python program utilizes OpenCV to detect faces in real-time from a webcam feed and provides various targeting options. It allows users to select different target styles such as F14 Style, Square, and Submarine, and provides distance estimation to the detected face in feet.

## Features

- Real-time face detection using OpenCV.
- Distance estimation from the camera to the detected face in feet.
- Three targeting options: F14 Style, Square, and Submarine.
- Target locked message displayed when a face is detected.
- Ability to eliminate the target with a key press.
- Explosion effect displayed upon target elimination.

## Prerequisites

- Python 3.x
- OpenCV
- NumPy

## Usage

1. Clone the repository to your local machine

2. Navigate to the project directory

3. Install the required dependencies:
pip install -r requirements.txt

4. Run the Python script

5. Press the following keys to interact with the program:

- `1`: Select F14 Style target.
- `2`: Select Square target (default).
- `3`: Select Submarine target.
- `Spacebar`: Eliminate the target.
- `q`: Quit the program.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
