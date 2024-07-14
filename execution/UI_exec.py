import tkinter as tk
from tkinter import messagebox

# Function to save the user-defined regex to a separate file
def save_regex(regex):
    with open('user_defined_regex.py', 'w') as f:
        f.write(f"USER_DEFINED_REGEX = r'{regex}'")

# Function to start monitoring the log file
def start_monitoring():
    log_file = log_file_entry.get()
    regex = regex_entry.get()
    save_regex(regex)
    with open('log_config.py', 'w') as f:
        f.write(f"LOG_FILE = '{log_file}'\n")
    messagebox.showinfo("Info", "Configuration saved! You can now run the monitoring script.")

# Setting up the UI
root = tk.Tk()
root.title("Log Monitoring Configuration")

tk.Label(root, text="Log File Path:").grid(row=0, column=0, padx=10, pady=5)
log_file_entry = tk.Entry(root, width=50)
log_file_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Log Regex Pattern:").grid(row=1, column=0, padx=10, pady=5)
regex_entry = tk.Entry(root, width=50)
regex_entry.grid(row=1, column=1, padx=10, pady=5)

start_button = tk.Button(root, text="Save Configuration", command=start_monitoring)
start_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
