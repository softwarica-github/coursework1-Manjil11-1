import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.constants import END
from tkinter import messagebox
from tkinter import filedialog
import re
from scanning_function import ScanningFunction
import sys

class EnumerationInterface(tk.Frame):
    def __init__(self, master, dashboard):
        super().__init__(master)
        self.dashboard = dashboard  # Assign the dashboard parameter to self.dashboard
        self.master = master
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

        ttk.Label(self.frame_header, text="NIKTO", style='Header.TLabel', font="didot 50 bold ").grid(row=0, column=1,
                                                                                                        padx=10, pady=10,
                                                                                                        sticky='sw')

        # Frame 2
        self.frame_content = ttk.Frame(self.main_frame)
        self.frame_content.pack(side=tk.TOP, pady=10)

        ttk.Label(self.frame_content, text="Enter Target URL or IP Address: ",
                  font=('didot 20 bold italic')).grid(row=0, column=0, padx=10, pady=15)

        self.entry_name = ttk.Entry(self.frame_content, width=35)
        self.entry_name.grid(row=1, column=0, padx=10)

        # Additional features: Scanning profiles
        self.scanning_profiles = {
            "Default": "-maxtime 5 -Tuning 0123456789abcde",
            "Web Server": "-maxtime 2 -Tuning 0123456789abcde",
            "Web Application": "--maxtime 2 -port 80 -id \"CustomHeader:Value\"",
            "Web Scraping": "-Plugins @webapp -Format txt",
            "Subdomain Enumeration": "-maxtime 2",
        }

        self.selected_profile = tk.StringVar()
        self.selected_profile.set("Default")

        ttk.Label(self.frame_content, text="Scanning Profile: ", font=('didot 20 bold italic')).grid(row=2, column=0,
                                                                                                     padx=10, pady=15)

        profile_dropdown = ttk.OptionMenu(self.frame_content, self.selected_profile, *self.scanning_profiles.keys())
        profile_dropdown.grid(row=2, column=1, padx=3, pady=7, sticky='w')

        # Frame 3
        self.frame_report = ttk.Frame(self.main_frame)
        self.frame_report.pack(side=tk.TOP, pady=10)

        self.txt = tk.Text(self.frame_report, width=100, height=15, font=('didot 20 bold italic'))
        self.txt.pack(side=tk.TOP, padx=10, pady=10)

        # Set the widget to be read-only
        self.txt.insert(0.0, 'Enumeration Scanning Report will appear here...')   
        self.txt.config(state=tk.DISABLED)

        # Buttons
        ttk.Button(self.frame_content, text="Scan", command=self.dscan, width=10).grid(row=5, column=0, padx=5,
                                                                                        pady=10, sticky='e')
        ttk.Button(self.frame_content, text="Clear", command=self.clear_text, width=10).grid(row=5, column=1, padx=5,
                                                                                         pady=10, sticky='w')
        ttk.Button(self.frame_content, text="Save Result", command=self.save_result, width=12).grid(row=5, column=2,
                                                                                                   padx=5, pady=10,
                                                                                                   sticky='e')
        self.style.configure('TCheckbutton', font=('didot 20 bold italic'))  # Set the font for the Checkbutton

        # Exit button
        ttk.Button(self.frame_report, text="Exit", command=self.exit_program, width=10).pack(side=tk.RIGHT, padx=10, pady=15)
        

        # Back button
        ttk.Button(self.frame_report, text="Back", command=self.back_to_dashboard, width=10).pack(side=tk.LEFT, padx=10, pady=15)


    def validate_input(self, input_str):
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        url_pattern = r"^(?:http[s]?:\/\/)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,3}){1,2}$"
        ip_valid = re.match(ip_pattern, input_str)
        url_valid = re.match(url_pattern, input_str)
        return ip_valid or url_valid

    def dscan(self):
        self.txt.configure(state=tk.NORMAL)
        self.txt.delete("1.0", tk.END)
        self.txt.insert(tk.END, 'Enumeration Scanning Report will appear here...')
        self.txt.configure(state=tk.DISABLED)

        input_str = self.entry_name.get()
        if not self.validate_input(input_str):
            messagebox.showerror("Error", "Invalid URL or IP address")
            return

        selected_profile = self.selected_profile.get()
        profile_options = self.scanning_profiles[selected_profile].split()
        scanning_function = ScanningFunction(self.txt)
        if selected_profile == "Web Scraping":
            scanning_function.perform_web_scraping(input_str)
        elif selected_profile == "Subdomain Enumeration":
            scanning_function.perform_subdomain_enumeration(input_str)
        else:
            scanning_function.run_nikto(input_str, profile_options)

    def save_result(self):
        # Get the result from the text widget
        result = self.txt.get("1.0", "end-1c")

        # Check if the result is empty or contains the default text
        if not result or result == 'Enumeration Scanning Report will appear here...':
            messagebox.showerror("Error", "No scanning result to save.")
            return

        # Open a file dialog to choose the save location
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            # Write the result to the chosen file
            with open(file_path, "w") as file:
                file.write(result)

    def back_to_dashboard(self):
        self.dashboard.master.deiconify()  # Show the dashboard window
        self.master.destroy()  # Close the EnumerationInterface window
    
    def start_enumeration(self):
        self.master.withdraw()  # Hide the dashboard window
        enumeration_window = tk.Toplevel(self.master)
        enumeration_window.protocol("WM_DELETE_WINDOW", self.back_to_dashboard)
        self.enumeration_window = enumeration_window  # Assign the created window to the attribute
        enumeration = EnumerationInterface(enumeration_window, self)

    def exit_program(self):
        self.master.destroy()  # Close the EnumerationInterface window
        sys.exit()  # Stop program execution


    def clear_text(self):
        self.txt.configure(state=tk.NORMAL)
        self.txt.delete('1.0', tk.END)
        self.txt.insert(tk.END, 'Enumeration Scanning Report will appear here...')
        self.txt.configure(state=tk.DISABLED)

    def clear(self):
        self.entry_name.delete(0, 'end')
        self.txt.configure(state=tk.NORMAL)
        self.txt.delete(0.0, 'end')
        self.txt.insert(0.0, 'Enumeration Scanning Report will appear here...')
        self.txt.configure(state=tk.DISABLED)
