from typing import Generator, List
import face_recognition
import os
import _thread
import asyncio
from time import sleep
import subprocess


def checkImageInSubprocess(ref, targets):
    for i in targets:
        if i.endswith(".png") or i.endswith(".jpeg") or i.endswith(".jpg"):
            subprocess.call(["py", "faceMatch.py", ref, i], cwd = os.getcwd())


ref = "registeredPics\\103\\image.png"
target = "D:\\Camera"

counter = 1
batchSize = 3
files = os.listdir(target)
for i in range(0, len(files)-batchSize, batchSize):
    
    if counter % batchSize == 0:
        print(f"sleeping for {batchSize**2} seconds")
        sleep(batchSize**2)

    file = [os.path.join(target, j) for j in files[i:i+batchSize]]
    _thread.start_new_thread(checkImageInSubprocess, (ref, file))

    counter += 1