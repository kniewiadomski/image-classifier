import tkinter as tk
from tkinter import ttk, messagebox

class SetupView(ttk.Frame):
    def __init__(self, parent, select_folder_callback, start_classification_callback):
        super().__init__(parent, padding="20")
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Center container
        center_frame = ttk.Frame(self)
        center_frame.grid(row=0, column=0)
        self.grid_columnconfigure(0, weight=1)  # Center horizontally
        self.grid_rowconfigure(0, weight=1)     # Center vertically
        
        # Class entry
        class_frame = ttk.LabelFrame(center_frame, text="Add New Class", padding="10")
        class_frame.grid(row=0, column=0, pady=10)
        
        ttk.Label(class_frame, text="Class name:", width=10).grid(row=0, column=0, padx=5)
        self.class_entry = ttk.Entry(class_frame, width=30)
        self.class_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(class_frame, text="Shortcut:", width=8).grid(row=0, column=2, padx=5)
        self.shortcut_entry = ttk.Entry(class_frame, width=5)
        self.shortcut_entry.grid(row=0, column=3, padx=5)
        
        add_button = ttk.Button(class_frame, text="Add Class", command=self.add_class, width=15)
        add_button.grid(row=0, column=4, padx=10)

        # Class list frame
        list_frame = ttk.LabelFrame(center_frame, text="Defined Classes", padding="10")
        list_frame.grid(row=1, column=0, pady=10)

        # Class list with scrollbar
        self.class_listbox = tk.Listbox(list_frame, height=8, width=50)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.class_listbox.yview)
        self.class_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.class_listbox.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Remove button
        remove_button = ttk.Button(list_frame, text="Remove Selected", command=self.remove_selected, width=20)
        remove_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Folder selection frame
        folder_frame = ttk.LabelFrame(center_frame, text="Image Folder", padding="10")
        folder_frame.grid(row=2, column=0, pady=10)

        select_button = ttk.Button(folder_frame, text="Select Folder", 
                                 command=select_folder_callback, width=15)
        select_button.grid(row=0, column=0, padx=5)
        
        self.folder_label = ttk.Label(folder_frame, text="No folder selected", 
                                    background='white', padding="5", width=50)
        self.folder_label.grid(row=0, column=1, padx=10)

        # Start button
        start_button = ttk.Button(center_frame, text="Start Classification", 
                                command=start_classification_callback, width=25)
        start_button.grid(row=3, column=0, pady=20)

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