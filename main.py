import tkinter as tk
from tkinter import filedialog
from file_organizer import FileOrganizer

def select_folder(prompt="Select folder"):
    root = tk.Tk()
    root.withdraw()  # ซ่อนหน้าต่างหลัก
    print(prompt)
    folder = filedialog.askdirectory(title=prompt)
    if not folder:
        print("\033[91m❌ Folder not selected. Exiting.\033[0m")
        exit(1)
    return folder

if __name__ == "__main__":
    source_dir = select_folder("📂 Select source folder (e.g. Google Photos)")
    dest_dir = select_folder("📁 Select destination folder")

    try:
        organizer = FileOrganizer(source_dir, dest_dir)
        organizer.organize_files()
        print("\033[92m✅ File organization completed successfully.\033[0m")
    except Exception as e:
        print(f"\033[91m❌ An error occurred: {e}\033[0m")
        exit(1)
