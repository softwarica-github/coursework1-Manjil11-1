import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from PIL import Image, ImageTk
from enumeration_gui import EnumerationInterface
from scanning_function import ScanningFunction
import sys


class DashboardInterface:
    def __init__(self, master):
        self.master = master
        master.title('NIKTO Dashboard')
        master.configure(background="#f2f2f2")
        self.enumeration_window = None  # Initialize the enumeration_window attribute

        self.style = ttk.Style()
        self.style.configure('TFrame', background="#f2f2f2")
        self.style.configure('TButton', background="#fff")
        self.style.configure('TLabel', background="#f2f2f2")
        self.style.configure('TSeparator', background="#f2f2f2")
        self.style.configure('Header.TLabel', font=('didot 20 bold italic'), background="#f2f2f2")

        # Create a main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame 1
        self.frame_header = ttk.Frame(self.main_frame)
        self.frame_header.pack(side=tk.TOP, pady=10)

        ttk.Label(self.frame_header, text="NIKTO", style='Header.TLabel', font="didot 40 bold ").grid(row=0, column=1,
                                                                                                        padx=10, pady=10,
                                                                                                        sticky='sw')


        # Frame 2
        self.frame_content = ttk.Frame(self.main_frame)
        self.frame_content.pack(side=tk.TOP, pady=10)

        ttk.Label(self.frame_content, text="Welcome to NIKTO Dashboard!", font=('didot 20 bold italic')).grid(row=0, column=0, padx=10, pady=15)


        # Load and display the image
        image_path = "/Users/manzil/Desktop/Pr0t3ct-main/web/image/hacker.jpg"
        if os.path.isfile(image_path):
            img = Image.open(image_path)
            self.photo = ImageTk.PhotoImage(img)
            image_label = ttk.Label(self.frame_content, image=self.photo)
            image_label.grid(row=1, column=0, padx=10, pady=10)
        else:
            print(f"Image not found: {image_path}")


        # Buttons
        self.start_enumeration_button = ttk.Button(self.frame_content, text="Start Enumeration", command=self.start_enumeration, width=15)
        self.start_enumeration_button.grid(row=2, column=0, padx=10, pady=10)

    def start_enumeration(self):
        self.master.withdraw()  # Hide the dashboard window
        enumeration_window = tk.Toplevel(self.master)
        enumeration_window.protocol("WM_DELETE_WINDOW", self.exit_program)  # Updated attribute name
        self.enumeration_window = enumeration_window  # Assign the created window to the attribute
        enumeration = EnumerationInterface(enumeration_window, self)


    def back_to_dashboard(self):
        if self.enumeration_window is not None and self.enumeration_window.winfo_exists():
            self.enumeration_window.destroy()  # Close the enumeration window
        self.master.destroy()  # Close the dashboard window
        sys.exit()  # Stop program execution

    def exit_program(self):
        if self.enumeration_window is not None and self.enumeration_window.winfo_exists():
            self.enumeration_window.destroy()  # Close the enumeration window
        self.master.destroy()  # Close the dashboard window
        sys.exit()  # Stop program execution

