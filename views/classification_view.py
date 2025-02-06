import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ClassificationView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        self.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.grid_remove()  # Hide initially

        # Image display
        self.image_label = ttk.Label(self)
        self.image_label.grid(row=0, column=0, columnspan=2)

        # Instructions label
        self.instructions = ttk.Label(self, text="Press the shortcut key to classify the image")
        self.instructions.grid(row=1, column=0, columnspan=2, pady=10)

        # Class reference
        self.class_reference = ttk.Label(self, text="Available classes:")
        self.class_reference.grid(row=2, column=0, columnspan=2)

    def show_image(self, image_path):
        image = Image.open(image_path)
        display_size = (600, 400)
        image.thumbnail(display_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference

    def update_class_reference(self, classes):
        reference_text = "Available classes:\n" + "\n".join(
            f"{shortcut}: {name}" for number, (shortcut, name) in classes.items()
        )
        self.class_reference.config(text=reference_text) 