# Image Classifier

A lightweight Python-based desktop application for rapid image classification into user-defined categories. This tool allows users to quickly label images by assigning keyboard shortcuts to classes for fast classification.

## Features

- Simple and intuitive user interface
- Custom class definition with keyboard shortcuts
- Single-key classification for rapid labeling
- Batch image processing from a selected folder
- Exports classifications to CSV format
- Supports common image formats (PNG, JPG, JPEG, GIF, BMP)

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/image-classifier.git
cd image-classifier
```

2. Install required dependencies:
```
pip install -r requirements.txt
```

## Usage

1. Run the application:
```
python main.py
```

2. In the setup screen:
   - Enter a class name (e.g., "cat")
   - Enter a single-character shortcut key (e.g., "c")
   - Click "Add Class" to add it to the list
   - Repeat for all needed classes
   - You can remove classes from the list if needed
   - Click "Select Image Folder" to choose the folder containing your images
   - Click "Start Classification" to begin

3. In the classification screen:
   - Images will be displayed one at a time
   - Press the corresponding shortcut key to assign a class to the current image
   - The application will automatically move to the next image
   - Available classes and their shortcuts are displayed for reference

4. When finished:
   - A `classifications.csv` file will be created in the image folder
   - The CSV will contain two columns: filename and class name

## Requirements

- Python 3.6 or higher
- Pillow (PIL Fork)
- tkinter (usually comes with Python)