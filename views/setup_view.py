import tkinter as tk
from tkinter import ttk, messagebox

class SetupView(ttk.Frame):
    def __init__(self, parent, select_folder_callback, start_classification_callback):
        super().__init__(parent, padding="10")
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Class entry
        class_frame = ttk.Frame(self)
        class_frame.grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Label(class_frame, text="Class name:").grid(row=0, column=0, padx=5)
        self.class_entry = ttk.Entry(class_frame, width=20)
        self.class_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(class_frame, text="Shortcut key:").grid(row=0, column=2, padx=5)
        self.shortcut_entry = ttk.Entry(class_frame, width=5)
        self.shortcut_entry.grid(row=0, column=3, padx=5)
        
        ttk.Button(class_frame, text="Add Class", command=self.add_class).grid(row=0, column=4, padx=5)

        # Class list
        ttk.Label(self, text="Defined Classes:").grid(row=1, column=0, columnspan=2, pady=(10,0))
        self.class_listbox = tk.Listbox(self, height=6, width=40)
        self.class_listbox.grid(row=2, column=0, columnspan=2)
        
        # Remove button
        ttk.Button(self, text="Remove Selected", command=self.remove_selected).grid(row=3, column=0, columnspan=2, pady=5)

        # Folder selection
        ttk.Button(self, text="Select Image Folder", command=select_folder_callback).grid(row=4, column=0)
        self.folder_label = ttk.Label(self, text="No folder selected")
        self.folder_label.grid(row=4, column=1)

        # Start button
        ttk.Button(self, text="Start Classification", command=start_classification_callback).grid(row=5, column=0, columnspan=2, pady=10)

        # Store callbacks
        self.on_add_class = None
        self.on_remove_class = None

    def set_class_callbacks(self, add_callback, remove_callback):
        self.on_add_class = add_callback
        self.on_remove_class = remove_callback

    def add_class(self):
        class_name = self.class_entry.get().strip()
        shortcut = self.shortcut_entry.get().strip().lower()
        
        if not class_name:
            messagebox.showerror("Error", "Please enter a class name")
            return
        if not shortcut:
            messagebox.showerror("Error", "Please enter a shortcut key")
            return
        if len(shortcut) != 1:
            messagebox.showerror("Error", "Shortcut must be a single character")
            return
            
        if self.on_add_class:
            try:
                number = self.on_add_class(class_name, shortcut)
                self.class_listbox.insert(tk.END, f"{number}: {class_name} ({shortcut})")
                self.class_entry.delete(0, tk.END)
                self.shortcut_entry.delete(0, tk.END)
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def remove_selected(self):
        selection = self.class_listbox.curselection()
        if selection and self.on_remove_class:
            index = selection[0]
            item_text = self.class_listbox.get(index)
            number = int(item_text.split(':')[0])
            self.on_remove_class(number)
            self.class_listbox.delete(index)

    def update_folder_label(self, folder_path):
        self.folder_label.config(text=folder_path) 