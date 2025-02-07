import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ClassificationView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="20")
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.grid_remove()  # Hide initially

        # Configure grid weights for centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Center container
        center_frame = ttk.Frame(self)
        center_frame.grid(row=0, column=0)
        
        # Create a horizontal layout frame
        content_frame = ttk.Frame(center_frame)
        content_frame.grid(row=0, column=0, pady=10)
        
        # Left side - Image
        left_frame = ttk.Frame(content_frame)
        left_frame.grid(row=0, column=0, padx=20)
        
        # Image display with frame
        image_frame = ttk.LabelFrame(left_frame, text="Current Image", padding="10")
        image_frame.grid(row=0, column=0, pady=5)

        # Set a fixed size for the image display area
        self.image_label = ttk.Label(image_frame, borderwidth=2, relief="solid")
        self.image_label.grid(row=0, column=0)
        
        # Fixed size for image display
        self.image_width = 640
        self.image_height = 480

        # Instructions label under image
        self.instructions = ttk.Label(left_frame, 
                                    text="Press the shortcut key to classify the image",
                                    font=('Arial', 12, 'bold'))
        self.instructions.grid(row=1, column=0, pady=15)

        # Right side - Classes
        right_frame = ttk.LabelFrame(content_frame, text="Available Classes", padding="15")
        right_frame.grid(row=0, column=1, padx=20, sticky="n")

        # Class reference with larger font and more spacing
        self.class_reference = ttk.Label(right_frame, 
                                       justify=tk.LEFT,
                                       font=('Arial', 14))
        self.class_reference.grid(row=0, column=0, padx=10)

        # Set some example text to show the layout
        self.class_reference.config(text="1: Cat (press 'c')\n\n"
                                       "2: Dog (press 'd')\n\n"
                                       "3: Bird (press 'b')\n\n"
                                       "4: Fish (press 'f')")

    def update_class_reference(self, classes):
        # Format class reference text with extra spacing between lines
        ref_text = "\n\n".join([f"{num}: {name} (press '{shortcut}')" 
                               for num, (name, shortcut) in classes.items()])
        self.class_reference.config(text=ref_text)

    def show_image(self, image_path):
        image = Image.open(image_path)
        display_size = (self.image_width, self.image_height)
        image.thumbnail(display_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference 