import os
import shutil
from datetime import datetime

SOURCE_DIR = 'D:\\learn\\test\\fileCopy'
DEST_ROOT = 'D:\\learn\\test\\filePatse'


def get_create_date(file_path):
    try:
        # ใช้ create date ของระบบไฟล์
        timestamp = os.path.getctime(file_path)
        return datetime.fromtimestamp(timestamp)
    except Exception:
        return None

def organize_files_by_date(source_dir):
    print(f"Starting file organization from {source_dir}...")
    for foldername, _, filenames in os.walk(source_dir):
        print(f"Scanning folder: {foldername}")
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            try:
                date = get_create_date(file_path)
                if date is None:
                    continue
                year = str(date.year)
                month = str(date.month).zfill(2)
                
                # โฟลเดอร์ปลายทาง
                dest_folder = os.path.join(DEST_ROOT, year, month)
                os.makedirs(dest_folder, exist_ok=True)

                # ตรวจซ้ำชื่อไฟล์
                dest_file_path = os.path.join(dest_folder, filename)
                counter = 1
                while os.path.exists(dest_file_path):
                    name, ext = os.path.splitext(filename)
                    dest_file_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")
                    counter += 1

                shutil.copy2(file_path, dest_file_path)
                print(f"Copied: {file_path} -> {dest_file_path}")
            except Exception as e:
                print(f"Error copying {file_path}: {e}")

if __name__ == "__main__":
    organize_files_by_date(SOURCE_DIR)
