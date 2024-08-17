import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to update the attack setup files
def update_files(log_file_path, regex_pattern):
    attack_folders = ['execution', 'injection', 'session', 'phishing']
    
    # Paths to the setup files within each attack folder
    for attack in attack_folders:
        setup_file_path = os.path.join(attack, 'setup', f'{attack}.py')
        
        # Read the current content of the setup file
        with open(setup_file_path, 'r') as file:
            lines = file.readlines()
        
        # Update the LOG_FILE and regex pattern
        for i in range(len(lines)):
            if lines[i].startswith("LOG_FILE ="):
                lines[i] = f"LOG_FILE = '{log_file_path}'\n"
            elif lines[i].startswith("DEFAULT_REGEX ="):
                lines[i] = f"DEFAULT_REGEX = r'{regex_pattern}'\n"
        
        # Write the updated content back to the setup file
        with open(setup_file_path, 'w') as file:
            file.writelines(lines)

    messagebox.showinfo("Success", "Setup files have been updated successfully!")

# Function to open the file dialog for selecting the log file
def select_log_file():
    log_file_path = filedialog.askopenfilename(title="Select Log File")
    log_file_entry.delete(0, tk.END)
    log_file_entry.insert(0, log_file_path)

# Function to apply the updates
def apply_changes():
    log_file_path = log_file_entry.get()
    regex_pattern = regex_entry.get()
    
    if not log_file_path or not regex_pattern:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    update_files(log_file_path, regex_pattern)

# Initialize the Tkinter window
root = tk.Tk()
root.title("Attack Setup Configuration")

# UI elements for log file path selection
tk.Label(root, text="Log File Path:").grid(row=0, column=0, padx=10, pady=10)
log_file_entry = tk.Entry(root, width=40)
log_file_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_log_file).grid(row=0, column=2, padx=10, pady=10)

# UI elements for regex pattern input
tk.Label(root, text="Regex Pattern:").grid(row=1, column=0, padx=10, pady=10)
regex_entry = tk.Entry(root, width=40)
regex_entry.grid(row=1, column=1, padx=10, pady=10)
regex_entry.insert(0, r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "([A-Z]+) (.*?) HTTP/.*?" (\d+) (\d+)')  # Default pattern

# Apply changes button
tk.Button(root, text="Apply Changes", command=apply_changes).grid(row=2, column=0, columnspan=3, pady=20)

# Start the Tkinter event loop
root.mainloop()
