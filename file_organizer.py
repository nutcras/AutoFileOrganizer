import shutil
from pathlib import Path
from utils import get_create_date

class FileOrganizer:
    ALLOWED_EXTENSIONS = {
        # Images
        '.jpg', '.jpeg', '.png', '.webp',
        # Videos
        '.mp4', '.mov', '.avi', '.mkv', '.wmv', '.webm', '.3gp', '.m4v',
    }
    
    def __init__(self, source_dir: str | Path, dest_dir: str | Path):
        self.source_dir = Path(source_dir)
        self.dest_dir = Path(dest_dir)
        
    def organize_files(self):
        print(f"Starting file organization from {self.source_dir}...")
        
        for file_path in self.source_dir.rglob('*'):
            if not file_path.is_file():
                continue
            
            self._handle_file(file_path)
    
    def _handle_file(self, file_path: Path):
        try:
            if file_path.suffix.lower() not in self.ALLOWED_EXTENSIONS:
                return
            
            print(f"Found file: {file_path.name}")
            
            date = get_create_date(file_path)
            if not date:
                return
              
            dest_folder = self._create_destination_folder(date)
            dest_file_path = self._get_unique_destination_path(dest_folder, file_path.name)
            
            shutil.copy2(file_path, dest_file_path)
            print(f"\033[32mCopied: {file_path} -> {dest_file_path}\033[0m")
        except Exception as e:
            print(f"\033[91mError copying {file_path}: {e}\033[0m")
            
              
    def _create_destination_folder(self, date):
        year, month = str(date.year), str(date.month).zfill(2)
        dest_folder = self.dest_dir / year / month
        dest_folder.mkdir(parents=True, exist_ok=True)
        return dest_folder

    def _get_unique_destination_path(self, dest_folder: Path, file_name: str) -> Path:
        name = Path(file_name).stem
        suffix = Path(file_name).suffix
        dest_file_path = dest_folder / file_name
        
        counter = 1
        while dest_file_path.exists():
            dest_file_path = dest_folder / f"{name}_{counter}{suffix}"
            counter += 1
            
        return dest_file_path