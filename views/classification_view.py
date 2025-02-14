import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class ClassificationView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="20")
        self.root = parent.winfo_toplevel()  # Get the root window
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.grid_remove()  # Hide initially

        # Configure grid weights for resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Center container
        center_frame = ttk.Frame(self)
        center_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_rowconfigure(0, weight=1)
        
        # Content frame
        content_frame = ttk.Frame(center_frame)
        content_frame.grid(row=0, column=0, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.grid_columnconfigure(0, weight=3)  # Give more weight to image column
        content_frame.grid_columnconfigure(1, weight=1)  # Less weight to class list column
        
        # Left side - Image
        left_frame = ttk.Frame(content_frame)
        left_frame.grid(row=0, column=0, padx=20, sticky=(tk.W, tk.E, tk.N, tk.S))
        left_frame.grid_columnconfigure(0, weight=1)
        
        # Add fullscreen button
        self.fullscreen_button = ttk.Button(left_frame, text="Toggle Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_button.grid(row=0, column=0, pady=(0, 5))
        
        # Image display with frame
        image_frame = ttk.LabelFrame(left_frame, text="Current Image", padding="10")
        image_frame.grid(row=1, column=0, pady=5)

        # Set a fixed size for the image display area
        self.image_label = ttk.Label(image_frame, borderwidth=2, relief="solid")
        self.image_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Fixed size for image display
        self.image_width = 640
        self.image_height = 480

        # Add counter label after filename
        self.counter_label = ttk.Label(left_frame, text="", font=('Arial', 10))
        self.counter_label.grid(row=2, column=0, pady=(5, 0))  # Put it right after filename
        
        # Add filename label under image
        self.filename_label = ttk.Label(left_frame, text="", font=('Arial', 10))
        self.filename_label.grid(row=2, column=0, pady=(5, 15))
        
        # Move instructions label down one row
        self.instructions = ttk.Label(left_frame, 
                                    text="Press the shortcut key to classify the image",
                                    font=('Arial', 12, 'bold'))
        self.instructions.grid(row=3, column=0, pady=5)
        
        # Move buttons frame down one row
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.grid(row=4, column=0, pady=10)
        
        # Add Go Back button
        self.back_button = ttk.Button(buttons_frame, text="Go Back (B)", 
                                    command=self.go_back)
        self.back_button.grid(row=0, column=0, padx=5)
        
        # Move Save and Exit button to buttons frame
        self.save_exit_button = ttk.Button(buttons_frame, text="Save and Exit", 
                                         command=self.save_and_exit)
        self.save_exit_button.grid(row=0, column=1, padx=5)

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

        # Add new class frame in right_frame
        new_class_frame = ttk.LabelFrame(right_frame, text="Add New Class", padding="10")
        new_class_frame.grid(row=1, column=0, pady=(20, 0), sticky="ew")

        # Class name entry
        ttk.Label(new_class_frame, text="Class Name:").grid(row=0, column=0, padx=5, pady=5)
        self.new_class_name = ttk.Entry(new_class_frame)
        self.new_class_name.grid(row=0, column=1, padx=5, pady=5)

        # Shortcut entry
        ttk.Label(new_class_frame, text="Shortcut:").grid(row=1, column=0, padx=5, pady=5)
        self.new_class_shortcut = ttk.Entry(new_class_frame, width=5)
        self.new_class_shortcut.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Add class button
        add_class_button = ttk.Button(new_class_frame, text="Add Class", command=self.add_new_class)
        add_class_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Add fullscreen state and store content_frame reference
        self.is_fullscreen = False
        self.content_frame = content_frame
        self.right_frame = right_frame

    def update_class_reference(self, classes):
        """Update the class reference text with current classes"""
        reference_text = "Available Classes:\n\n"
        for number, (shortcut, name) in classes.items():
            reference_text += f"{name} (press {shortcut})\n"
        self.class_reference.config(text=reference_text)

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            # Restore normal view
            self.root.attributes('-fullscreen', False)
            self.right_frame.grid(row=0, column=1, padx=20, sticky="n")
            self.fullscreen_button.config(text="Toggle Fullscreen")
        else:
            # Enter fullscreen view
            self.root.attributes('-fullscreen', True)
            self.right_frame.grid_remove()
            self.fullscreen_button.config(text="Exit Fullscreen")
            
        self.is_fullscreen = not self.is_fullscreen
        
        # Force the window to update its layout
        self.root.update_idletasks()

    def show_image(self, image_path):
        self._current_image_path = image_path
        image = Image.open(image_path)
        display_size = (self.image_width, self.image_height)
        image.thumbnail(display_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference
        
        # Update filename label
        filename = os.path.basename(image_path)
        self.filename_label.config(text=f"File: {filename}")
        
        # Update counter
        total = len(self.classifier.image_files)
        current = self.classifier.current_image_index + 1
        self.counter_label.config(text=f"Image {current} of {total}")

    def add_new_class(self):
        class_name = self.new_class_name.get().strip()
        shortcut = self.new_class_shortcut.get().strip()
        
        if not class_name or not shortcut:
            messagebox.showerror("Error", "Both class name and shortcut are required")
            return
            
        try:
            number = self.classifier.add_class(class_name, shortcut)
            # Update the class reference text
            self.update_class_reference()
            # Clear the entry fields
            self.new_class_name.delete(0, tk.END)
            self.new_class_shortcut.delete(0, tk.END)
            messagebox.showinfo("Success", f"Added new class: {class_name} (shortcut: {shortcut})")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def save_and_exit(self):
        """Save current progress and return to setup view"""
        if messagebox.askyesno("Save and Exit", 
                              "Do you want to save current progress and exit?"):
            if hasattr(self, 'classifier') and self.classifier.save_and_exit():
                self.grid_remove()
                if hasattr(self, 'return_to_setup'):
                    self.return_to_setup()

    def go_back(self):
        """Go back to previous image"""
        if hasattr(self, 'classifier'):
            if self.classifier.go_back():
                # Update the display with the previous image
                image_path = self.classifier.get_current_image_path()
                if image_path:
                    self.show_image(image_path) 