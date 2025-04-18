from datetime import datetime
import os
import shutil
from utils import get_create_date

def organize_files_by_date(source_dir, DEST_ROOT):
    print(f"Starting file organization from {source_dir}...")
    for foldername, _, filenames in os.walk(source_dir):
        print(f"\033[33mScanning folder: {foldername}\033[0m")
        for filename in filenames:
            print(f"Found file: {filename}")
            file_path = os.path.join(foldername, filename)
            try:
                if filename.lower().endswith(('.json')):
                    continue
                else:
                    date = get_create_date(file_path) 

                # date = get_create_date(file_path)
                if date is None:
                    continue
                
                year = str(date.year)
                month = str(date.month).zfill(2)
                
                # # แยกโฟลเดอร์สำหรับไฟล์วิดีโอ
                # if filename.lower().endswith(('.mov', '.mp4', '.avi', '.mkv')):
                #     # หากเป็นไฟล์วิดีโอ, สร้างโฟลเดอร์แยก
                #     dest_folder = os.path.join(DEST_ROOT, 'videos', year, month)
                # else:
                #     # หากไม่ใช่ไฟล์วิดีโอ, ใช้โฟลเดอร์ตามปีและเดือน
                dest_folder = os.path.join(DEST_ROOT, year, month)

                os.makedirs(dest_folder, exist_ok=True)

                # ตรวจซ้ำชื่อไฟล์
                dest_file_path = os.path.join(dest_folder, filename)
                counter = 1
                while os.path.exists(dest_file_path):
                    name, ext = os.path.splitext(filename)
                    dest_file_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")
                    counter += 1

                shutil.copy2(file_path, dest_file_path)  # คัดลอกไฟล์
                print(f"\033[32mCopied: {file_path} -> {dest_file_path}\033[0m")
            except Exception as e:
                print(f"\033[91mError copying {file_path}: {e}\033[0m")

 