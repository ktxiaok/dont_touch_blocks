import PyInstaller.__main__
from send2trash import send2trash
import shutil
import os
from zipfile import ZipFile

OUTPUT_DIR_PATH = "./build/windows/DontTouchBlocks"
OUTPUT_ZIP_FILE_PATH = OUTPUT_DIR_PATH + ".zip"

if os.path.exists(OUTPUT_DIR_PATH):
    send2trash(OUTPUT_DIR_PATH)

PyInstaller.__main__.run((
    "main.py",
    "--workpath",
    "./build/work_files",
    "--distpath",
    OUTPUT_DIR_PATH,
    "--onefile",
    "--noconsole",
    "--name",
    "DontTouchBlocks"
))

shutil.copytree("./resources", os.path.join(OUTPUT_DIR_PATH, "resources"))

with ZipFile(OUTPUT_ZIP_FILE_PATH, "w") as zipobj:
    for rootpath, dirnames, filenames in os.walk(OUTPUT_DIR_PATH):
        for filename in filenames:
            fullpath = os.path.join(rootpath, filename)
            relpath = os.path.relpath(fullpath, OUTPUT_DIR_PATH)
            zipobj.write(fullpath, relpath)

print("Successful build!")
