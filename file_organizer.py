import os
import shutil
from utils import get_create_date

class FileOrganizer:
    def __init__(self, source_dir, dest_dir):
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        
    def organize_files(self):
        print(f"Starting file organization from {self.source_dir}...")
        
        for foldername, _, filenames in os.walk(self.source_dir):
            print(f"\033[33mScanning folder: {foldername}\033[0m")
            self._process_files(foldername, filenames)
    
    def _process_files(self, folder_name, file_names):
        for file_name in file_names:
            file_path = os.path.join(folder_name, file_name)
            print(f"Found file: {file_name}")
            
            if file_name.lower().endswith(('.json')):
                continue
              
            self._handle_file(file_path, file_name)
    
    def _handle_file(self, file_path, file_name):
        try:
            date = get_create_date(file_path)
            if not date:
                return
              
            dest_folder = self._create_destination_folder(date)
            dest_file_path = self._get_unique_destination_path(dest_folder, file_name)
            
            shutil.copy2(file_path, dest_file_path)
            print(f"\033[32mCopied: {file_path} -> {dest_file_path}\033[0m")
        except Exception as e:
            print(f"\033[91mError copying {file_path}: {e}\033[0m")
            
              
    def _create_destination_folder(self, date):
        year, month = str(date.year), str(date.month).zfill(2)
        dest_folder = os.path.join(self.dest_dir, year, month)
        os.makedirs(dest_folder, exist_ok=True)
        return dest_folder

    def _get_unique_destination_path(self, dest_folder, file_name):
        name, ext = os.path.splitext(file_name)
        dest_file_path = os.path.join(dest_folder, file_name)
        
        counter = 1
        while os.path.exists(dest_file_path):
            dest_file_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")
            counter += 1
            
        return dest_file_path