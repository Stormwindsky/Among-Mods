import os
import shutil
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox

def get_among_us_directory():
    # Possible paths for Among Us
    possible_paths = [
        os.path.join(os.environ.get('ProgramFiles(x86)', ''), 'Steam', 'steamapps', 'common', 'Among Us'),
        os.path.join(os.environ.get('ProgramFiles', ''), 'Steam', 'steamapps', 'common', 'Among Us'),
        os.path.join('C:', 'Steam', 'steamapps', 'common', 'Among Us')
    ]
    
    # Check if Among Us exists in any of the paths
    for path in possible_paths:
        if os.path.exists(path):
            return path
            
    # If not found, ask the user
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select the Among Us directory")
    return directory if directory else None

def create_modpack():
    # Ask if the user wants to create a modpack
    response = input("Do you want to create a modpack? (Yes/No) : ")
    if response.lower() not in ["yes", "y", "oui", "o"]:
        print("Cancelling modpack creation")
        return

    # Find the Among Us directory
    source_dir = get_among_us_directory()
    if not source_dir:
        print("Unable to find the Among Us directory")
        return

    # Ask for the modpack directory name
    folder_name = input("Enter the name of your modpack: ")
    
    # Create the destination directory in the same directory as Among Us
    dest_dir = os.path.join(os.path.dirname(source_dir), folder_name)
    
    try:
        # Copy the Among Us directory
        shutil.copytree(source_dir, dest_dir)
        
        # Create a shortcut on the desktop
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        shortcut_path = os.path.join(desktop, f"{folder_name}.lnk")
        
        with open(shortcut_path, "w") as f:
            exe_path = os.path.join(dest_dir, "Among Us.exe")
            f.write(f"[InternetShortcut]\nURL=file:///{exe_path.replace('\\', '/')}")
        
        # Interface for selecting zip files
        root = tk.Tk()
        root.withdraw()
        zip_files = filedialog.askopenfilenames(
            title="Select zip files",
            filetypes=[("Zip files", "*.zip")]
        )
        
        # Extract zip files
        for zip_file in zip_files:
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(dest_dir)
        
        # Show success message
        messagebox.showinfo("Success", "Modpack created successfully!\nTry your modded Among Us")
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    create_modpack()