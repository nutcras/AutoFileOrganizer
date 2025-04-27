import json
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS 
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

def get_create_date(image_path: Path | str):
    image_path = Path(image_path)
    json_path = find_metadata_file(image_path)
    if not json_path:
       return get_date_taken(image_path) 
    else:
       return get_date_from_json(json_path)


def get_date_taken(file_path: Path):
    ext = file_path.suffix.lower()

    if ext in ['.jpg', '.jpeg', '.png']:
        return get_image_date(file_path)
    elif ext in ['.mov', '.mp4', '.3gp']:
        return get_video_date(file_path)
    else:
        print(f"Unsupported file type: {file_path}")
        return get_create_date_last_update_date(file_path)

def get_video_date(file_path: Path):
    try:
        parser = createParser(str(file_path))
        if not parser:
            print(f"Unable to parse video file: {file_path}")
            return None

        with parser:
            metadata = extractMetadata(parser)
            if metadata and metadata.has("creation_date"):
                return metadata.get("creation_date")
    except Exception as e:
        print(f"Error reading video metadata from {file_path}: {e}")
    
    return get_create_date_last_update_date(file_path)

def get_image_date(file_path: Path):
    try:
        image = Image.open(file_path)
        exif_data = image.getexif()
        print(f"EXIF data: {exif_data}")
        if not exif_data or len(exif_data) == 0:
            return get_create_date_last_update_date(file_path)
        
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == 'DateTimeOriginal':
                date_str = value
                break
            elif tag == 'DateTime':
                date_str = value
        if date_str:
            return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Error reading EXIF from {file_path}: {e}")
    
    return get_create_date_last_update_date(file_path)

def get_create_date_last_update_date(image_path: Path):
    try:
        timestamp = image_path.stat().st_ctime
        return datetime.fromtimestamp(timestamp)
    except Exception as e:
        print(f"Error getting create date for {image_path}: {e}")
    return None

def get_date_from_json(json_path: Path):
    try:
        with json_path.open('r', encoding='utf-8') as f:
            data = json.load(f)

        timestamp = data.get("photoTakenTime", {}).get("timestamp")
        if timestamp:
            return datetime.fromtimestamp(int(timestamp))
    except Exception as e:
        print(f"\033[33mWarning reading JSON {json_path}: {e}\033[0m")
    return None
    

def find_metadata_file(image_path: Path):
    folder = image_path.parent
    image_name = image_path.name

    for f in folder.iterdir():
        if f.name.startswith(image_name) and f.suffix == '.json':
            return f

    image_name_no_ext = image_path.stem
    for f in folder.iterdir():
        if f.name.startswith(image_name_no_ext) and f.suffix == '.json':
            return f

    return None
