import PyInstaller.__main__
from send2trash import send2trash
import shutil
import os

OUTPUT_DIR_PATH = "./build/windows/DontTouchBlocks"

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

print("Successful build!")
