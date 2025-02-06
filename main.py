import tkinter as tk
from tkinter import filedialog, messagebox
from views.setup_view import SetupView
from views.classification_view import ClassificationView
from models.classifier import ImageClassifier

class ImageClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Classifier")
        self.root.geometry("800x600")

        self.classifier = ImageClassifier()
        
        # Create views
        self.setup_view = SetupView(
            root,
            self.select_folder,
            self.start_classification
        )
        # Set callbacks immediately after creating SetupView
        self.setup_view.set_class_callbacks(
            self.add_class,
            self.remove_class
        )
        
        self.classification_view = ClassificationView(root)

        # Bind keyboard events
        self.root.bind('<Key>', self.handle_key_press)

    def add_class(self, class_name, shortcut):
        try:
            return self.classifier.add_class(class_name, shortcut)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            raise

    def remove_class(self, number):
        self.classifier.remove_class(number)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            if self.classifier.load_images_from_folder(folder_path):
                self.setup_view.update_folder_label(folder_path)
            else:
                messagebox.showerror("Error", "No images found in selected folder")

    def start_classification(self):
        if not self.classifier.classes:
            messagebox.showerror("Error", "Please add at least one class")
            return
        if not self.classifier.image_folder:
            messagebox.showerror("Error", "Please select a folder")
            return

        # Switch to classification view
        self.setup_view.grid_remove()
        self.classification_view.grid()
        self.classification_view.update_class_reference(self.classifier.classes)
        self.show_next_image()

    def show_next_image(self):
        image_path = self.classifier.get_current_image_path()
        if image_path:
            self.classification_view.show_image(image_path)
        else:
            output_file = self.classifier.save_classifications()
            messagebox.showinfo("Complete", f"Classifications saved to {output_file}")
            self.root.quit()

    def handle_key_press(self, event):
        if self.classification_view.winfo_viewable():
            key = event.char.lower()
            class_number = self.classifier.get_class_by_shortcut(key)
            if class_number is not None:
                if self.classifier.classify_current_image(class_number):
                    self.show_next_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageClassifierApp(root)
    root.mainloop()
