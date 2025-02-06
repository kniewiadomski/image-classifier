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

    def load_images_from_folder(self, folder_path):
        self.image_folder = folder_path
        self.image_files = [f for f in os.listdir(self.image_folder) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
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
            self.classifications[self.image_files[self.current_image_index]] = self.classes[class_number]
            self.current_image_index += 1
            return True
        return False

    def get_current_image_path(self):
        if self.current_image_index < len(self.image_files):
            return os.path.join(self.image_folder, self.image_files[self.current_image_index])
        return None

    def save_classifications(self):
        output_file = os.path.join(self.image_folder, 'classifications.csv')
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['filename', 'class'])
            for filename, class_data in self.classifications.items():
                # class_data is a tuple of (shortcut, name), we only want the name
                writer.writerow([filename, class_data[1]])
        return output_file

    def add_class(self, class_name, shortcut):
        if shortcut in [data[0] for data in self.classes.values()]:
            raise ValueError("This shortcut is already in use")
        
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