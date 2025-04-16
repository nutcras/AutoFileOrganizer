# 📂 AutoFileOrganizer

**AutoFileOrganizer** is a smart file organizing script that scans all folders in a given drive, detects the creation date of every file, and **copies** them into folders grouped by **year** and **month**.

Whether you're a photographer, content creator, or just someone with a messy D: drive — TimeSorter helps you make sense of your digital chaos.

---

## 🔧 Features

- ✅ Organizes **all file types** — images, videos, documents, and more
- ✅ Uses **file creation date** to sort into folders like:  
  `D:\image\2025\04\...`
- ✅ **Recursively scans** all subfolders
- ✅ Automatically handles duplicate filenames with safe renaming
- ✅ **Does not delete or move original files**
- ✅ Lightweight, standalone script — no database or config needed

---


## Example Input
D:\
└── folder\***

## Example Output
D:\
└── image\
    ├── 2023\
    │   ├── 07\
    │   └── 08\
    ├── 2024\
    │   └── 12\
    └── 2025\
        ├── 01\
        └── 04\
