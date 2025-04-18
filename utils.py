import json
import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS 
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

def get_create_date(image_path):
    json_path = find_metadata_file(image_path)
    if not json_path:
       return get_date_taken(image_path) 
    else:
       return get_date_from_json(json_path)


def get_date_taken(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in ['.jpg', '.jpeg', '.png']:
        return get_image_date(file_path)
    elif ext in ['.mov', '.mp4', '.3gp']:
        return get_video_date(file_path)
    else:
        print(f"Unsupported file type: {file_path}")
        return get_create_date_last_update_date(file_path)

def get_video_date(file_path):
    try:
        parser = createParser(file_path)
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

def get_image_date(file_path):
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
            elif tag == 'DateTime':  # ใช้แทนถ้า Original ไม่มี
                date_str = value
        if date_str:
            return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Error reading EXIF from {file_path}: {e}")
    
    return get_create_date_last_update_date(file_path)

def get_create_date_last_update_date(image_path):
    try:
        timestamp = os.path.getctime(image_path)  
        return datetime.fromtimestamp(timestamp)
    except Exception as e:
        print(f"Error getting create date for {image_path}: {e}")
    return None

def get_date_from_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        timestamp = data.get("photoTakenTime", {}).get("timestamp")
        if timestamp:
            return datetime.fromtimestamp(int(timestamp))
    except Exception as e:
        print(f"\033[33mWarning reading JSON {json_path}: {e}\033[0m")
    return None
    

def find_metadata_file(image_path):
    folder = os.path.dirname(image_path)
    image_name = os.path.basename(image_path)

    for f in os.listdir(folder):
        if f.startswith(image_name) and f.endswith(".json"):
            return os.path.join(folder, f)

    # ลองจับคู่ชื่อแบบหลวม เช่น ไม่รวม .jpg
    image_name_no_ext = os.path.splitext(image_name)[0]
    for f in os.listdir(folder):
        if f.startswith(image_name_no_ext) and f.endswith(".json"):
            return os.path.join(folder, f)

    return None
