# Image Classifier

A lightweight Python-based desktop application for rapid image classification into user-defined categories. This tool allows users to quickly label images by assigning them to predefined classes using keyboard shortcuts.

## Features

- Simple and intuitive user interface
- Custom class definition with number mappings
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
pip install Pillow
```

## Usage

1. Run the application:
```
python main.py
```

2. In the setup screen:
   - Enter class names and their corresponding numbers (one per line)
   - Example format:
     ```
     cat 1
     dog 2
     bird 3
     ```
   - Click "Select Image Folder" to choose the folder containing your images
   - Click "Start Classification" to begin

3. In the classification screen:
   - Images will be displayed one at a time
   - Click the corresponding class button to assign a class to the current image
   - The application will automatically move to the next image

4. When finished:
   - A `classifications.csv` file will be created in the image folder
   - The CSV will contain two columns: filename and assigned class

## Requirements

- Python 3.6 or higher
- Pillow (PIL Fork)
- tkinter (usually comes with Python)