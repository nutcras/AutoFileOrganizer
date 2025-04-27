import os
import shutil
from utils import get_create_date

def organize_files_by_date(source_dir, dest_root):
    print(f"Starting file organization from {source_dir}...")
    
    for foldername, _, filenames in os.walk(source_dir):
        print(f"\033[33mScanning folder: {foldername}\033[0m")

        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            print(f"Found file: {filename}")

            if filename.lower().endswith(('.json')):
                continue

            try:
                date = get_create_date(file_path) 
                if not date:
                    continue

                year, month = str(date.year), str(date.month).zfill(2)

                dest_folder = os.path.join(dest_root, year, month)
                os.makedirs(dest_folder, exist_ok=True)

                # ตรวจซ้ำชื่อไฟล์
                dest_file_path = os.path.join(dest_folder, filename)
                name, ext = os.path.splitext(filename)

                counter = 1
                while os.path.exists(dest_file_path):
                    dest_file_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")
                    counter += 1

                shutil.copy2(file_path, dest_file_path)  # คัดลอกไฟล์
                print(f"\033[32mCopied: {file_path} -> {dest_file_path}\033[0m")
                
            except Exception as e:
                print(f"\033[91mError copying {file_path}: {e}\033[0m")

 