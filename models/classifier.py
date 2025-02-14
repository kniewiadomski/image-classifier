import csv
import os

class ImageClassifier:
    def __init__(self):
        self.classes = {}  # Dictionary to store class_name: (shortcut, number) pairs
        self.image_folder = ""
        self.image_files = []
        self.current_image_index = 0
        self.classifications = {}  # Dictionary to store filename: class pairs
        self.next_class_number = 1
        self.classification_history = []  # Add this to track history

    def load_existing_classifications(self):
        """Load existing classifications from CSV file"""
        csv_path = os.path.join(self.image_folder, 'classifications.csv')
        if not os.path.exists(csv_path):
            return {}
        
        existing = {}
        try:
            with open(csv_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                if 'filename' not in reader.fieldnames or 'class' not in reader.fieldnames:
                    return {}
                
                for row in reader:
                    existing[row['filename']] = row['class']
        except Exception as e:
            print(f"Error loading existing classifications: {e}")
            return {}
        
        return existing

    def load_images_from_folder(self, folder_path, skip_classified=False):
        """Load images from folder, optionally skipping classified ones"""
        self.image_folder = folder_path
        all_images = [f for f in os.listdir(self.image_folder) 
                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        
        if skip_classified:
            existing = self.load_existing_classifications()
            self.image_files = [img for img in all_images if img not in existing]
            print(f"Found {len(existing)} classified images, skipping them")
            print(f"Remaining unclassified images: {len(self.image_files)}")
        else:
            self.image_files = all_images
        
        self.current_image_index = 0
        self.classifications = {}
        self.classification_history = []
        
        return bool(self.image_files)

    def parse_classes(self, class_text):
        self.classes.clear()
        for line in class_text.split('\n'):
            if line.strip():
                name, number = line.strip().split()
                self.classes[int(number)] = (name, int(number))
        return bool(self.classes)

    def classify_current_image(self, class_number):
        if self.current_image_index < len(self.image_files):
            current_file = self.image_files[self.current_image_index]
            # Store the classification in history before moving forward
            self.classification_history.append((current_file, self.current_image_index))
            self.classifications[current_file] = self.classes[class_number]
            self.current_image_index += 1
            return True
        return False

    def get_current_image_path(self):
        if self.current_image_index < len(self.image_files):
            return os.path.join(self.image_folder, self.image_files[self.current_image_index])
        return None

    def save_and_exit(self):
        self.save_classifications()
        # Don't quit the application, just return to setup view
        return True

    def save_classifications(self):
        output_file = os.path.join(self.image_folder, 'classifications.csv')
        existing_classifications = self.load_existing_classifications()
        
        # Merge existing classifications with new ones
        all_classifications = existing_classifications.copy()
        all_classifications.update(self.classifications)
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['filename', 'class'])
            for filename, class_data in all_classifications.items():
                # Extract just the class name (second element of the tuple)
                class_name = class_data[1] if isinstance(class_data, tuple) else class_data
                writer.writerow([filename, class_name])
        return output_file

    def add_class(self, class_name, shortcut):
        if shortcut in [data[0] for data in self.classes.values()]:
            raise ValueError("This shortcut is already in use")
        
        # Check if class name already exists
        if class_name in [data[1] for data in self.classes.values()]:
            raise ValueError("This class name already exists")
        
        number = self.next_class_number
        self.classes[number] = (shortcut, class_name)
        self.next_class_number += 1
        return number

    def remove_class(self, number):
        if number in self.classes:
            del self.classes[number]

    def get_class_by_shortcut(self, shortcut):
        for number, (key, name) in self.classes.items():
            if key == shortcut:
                return number

    def go_back(self):
        """Go back to the previous image"""
        if not self.classification_history:
            return False
            
        # Remove the last classification
        last_file, last_index = self.classification_history.pop()
        if last_file in self.classifications:
            del self.classifications[last_file]
        
        # Go back to the previous image
        self.current_image_index = last_index
        return True 