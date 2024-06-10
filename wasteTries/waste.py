from typing import List
import face_recognition
import os
import asyncio
from threading import Lock
import _thread

class ImageMatcher:
    def __init__(self, sourceImagePath, targetDirPath) -> None:
        self.sourceImagePath = sourceImagePath
        self.targetDirPath = targetDirPath
        self.imageTypes = ["jpg", "png", "jpeg"]
        self.matchmaking = False
        self.matchedImages = []
        self.lock = Lock()

        # Load and encode the known image
        print(f"Loading known image from {self.sourceImagePath}")
        self.known_image = face_recognition.load_image_file(self.sourceImagePath)
        known_encodings = face_recognition.face_encodings(self.known_image)
        if len(known_encodings) == 0:
            raise ValueError("No faces found in the source image.")
        self.known_encoding = known_encodings[0]

    def getTargetImageFilePaths(self) -> List[str]:
        print(f"Listing files in directory {self.targetDirPath}")
        files: List[str] = os.listdir(self.targetDirPath)
        image_files = []
        for file in files:
            for ext in self.imageTypes:
                if file.lower().endswith(f".{ext}"):
                    image_files.append(os.path.join(self.targetDirPath, file))
                    break
        print(f"Found {len(image_files)} image files")
        return image_files

    async def imagesMatch(self, targetImage: str, semaphore: asyncio.Semaphore) -> bool:
        async with semaphore:
            try:
                print(f"Processing image {targetImage}")
                unknown_image = face_recognition.load_image_file(targetImage)
                unknown_encodings = face_recognition.face_encodings(unknown_image, model="small")
                num_faces = len(unknown_encodings)
                print(f"Found {num_faces} faces in {targetImage}")

                if num_faces == 0:
                    return False

                unknown_encoding = unknown_encodings[0]
                matched = any(face_recognition.compare_faces([self.known_encoding], unknown_encoding))

                print(f"Match status for {targetImage}: {matched}")

                if matched:
                    with self.lock:
                        self.matchedImages.append(targetImage)
                    print(f"Match found: {targetImage}")
                
                return matched
            except Exception as e:
                print(f"Error processing image {targetImage}: {e}")
                return False

    async def searchAll(self, batch_size=10):
        imgFiles = self.getTargetImageFilePaths()
        semaphore = asyncio.Semaphore(batch_size)  # Limit concurrent tasks

        tasks = [asyncio.run(self.imagesMatch(imgFile, semaphore)) for imgFile in imgFiles]

        # _thread.start_new_thread(asyncio.run, asyncio.gather(*tasks))

        print("Matched:", self.matchedImages)

# Usage example:
matchMyFace = ImageMatcher("registeredPics\\103\\image.png", "D:\\Camera")
asyncio.run(matchMyFace.searchAll(batch_size=10))
