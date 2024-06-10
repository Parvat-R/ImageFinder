from typing import Generator, List
import face_recognition
import os
import threading
import asyncio
from time import sleep

lock = threading.Lock()

class ImageMatcher:
    def __init__(self, sourceImagePath, targerDirPath) -> None:
        self.sourceImagePath = sourceImagePath
        self.targetDirPath = targerDirPath
        self.imageTypes = ["jpg", "png", "jpeg"]
        self.matchmaking = False
        self.matchedImages = []
        self.known_image = face_recognition.load_image_file(self.sourceImagePath)
        self.known_encoding = face_recognition.face_encodings(self.known_image)[0]

    def getTargetImageFilePaths(self):
        files: List[str] = os.listdir(self.targetDirPath)
        for file in files:
            for ext in self.imageTypes:
                if f".{ext}" in file.lower().strip():
                    yield os.path.join(self.targetDirPath, file)
                    break


    def imagesMatch(self, targetImage: str) -> bool:
        unknown_image = face_recognition.load_image_file(targetImage)
        unknown_encodings = face_recognition.face_encodings(unknown_image, model = "small")
        if len(unknown_encodings) > 0:
            for unknown_encoding in unknown_encodings:
                matched = any(face_recognition.compare_faces([self.known_encoding], unknown_encoding))
                if matched:
                    print("found")
                    self.matchedImages.append(targetImage)
                break
            return matched
        else: None


    def searchAll(self):
        imgFiles = self.getTargetImageFilePaths()
        result = []
        for imgFile in imgFiles:
            result.append(self.imagesMatch(imgFile))

        print(result)
        return result

matchMyFace = ImageMatcher("registeredPics\\103\\image.png", "D:\\Camera")
matchMyFace.searchAll()