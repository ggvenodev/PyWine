import tkinter as tk
from tkinter import messagebox
import subprocess
from os import system
import os
def save_config():
    token = token_entry.get()
    user_id = user_id_entry.get()
    channel_id = channel_id_entry.get()
    process_name = process_name_entry.get()

    if not token or not user_id or not channel_id or not process_name:
        messagebox.showerror("Input Error", "All fields must be filled out.")
        return

    try:
        # Open the original script and read its contents
        with open('source.py', 'r') as file:
            script_content = file.read()

        # Replace the placeholders with user input
        script_content = script_content.replace('TOKEN_HERE', token)
        script_content = script_content.replace('11111', user_id)
        script_content = script_content.replace('22222', channel_id)

        # Save the modified script as a new file
        configured_script = 'configured_bot.pyw'
        with open(configured_script, 'w') as file:
            file.write(script_content)

        # Create the executable using PyInstaller
        subprocess.run(['pyinstaller', '--onefile', '--name', process_name, configured_script], check=True)
        os.system("DEL configured_bot.pyw")
        os.system(f"DEL {process_name}.spec")

        messagebox.showinfo("Success", "Configuration saved and executable created successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Discord Bot Configurator")

# Set dark mode colors
bg_color = "#2e2e2e"
fg_color = "#ffffff"
entry_bg_color = "#3a3a3a"
entry_fg_color = "#ffffff"
button_bg_color = "#4a4a4a"
button_fg_color = "#ffffff"

# Apply dark mode colors to the main window
root.configure(bg=bg_color)

# Create and place labels and entry fields with dark mode styling
tk.Label(root, text="Discord Bot Token:", bg=bg_color, fg=fg_color).grid(row=0, column=0, padx=10, pady=10)
token_entry = tk.Entry(root, width=50, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
token_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Your Discord User ID:", bg=bg_color, fg=fg_color).grid(row=1, column=0, padx=10, pady=10)
user_id_entry = tk.Entry(root, width=50, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
user_id_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Discord Channel ID:", bg=bg_color, fg=fg_color).grid(row=2, column=0, padx=10, pady=10)
channel_id_entry = tk.Entry(root, width=50, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
channel_id_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Process Name:", bg=bg_color, fg=fg_color).grid(row=3, column=0, padx=10, pady=10)
process_name_entry = tk.Entry(root, width=50, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
process_name_entry.grid(row=3, column=1, padx=10, pady=10)

# Create and place the save button with dark mode styling
save_button = tk.Button(root, text="Save Configuration", bg=button_bg_color, fg=button_fg_color, command=save_config)
save_button.grid(row=4, column=0, columnspan=2, pady=20)

# Run the Tkinter event loop
root.mainloop()
