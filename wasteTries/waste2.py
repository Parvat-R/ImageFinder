from typing import List
import face_recognition
import os
import asyncio
import concurrent
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

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

    def imagesMatch(self, targetImage: str) -> bool:
        try:
            known_image = face_recognition.load_image_file(self.sourceImagePath)
            known_encodings = face_recognition.face_encodings(known_image)
            if len(known_encodings) == 0:
                raise ValueError("No faces found in the source image.")
            known_encoding = known_encodings[0]
            print(f"Processing image {targetImage}")
            unknown_image = face_recognition.load_image_file(targetImage)
            unknown_encodings = face_recognition.face_encodings(unknown_image, model="small")
            num_faces = len(unknown_encodings)
            print(f"Found {num_faces} faces in {targetImage}")

            if num_faces == 0:
                return False

            unknown_encoding = unknown_encodings[0]
            matched = any(face_recognition.compare_faces([known_encoding], unknown_encoding))

            print(f"Match status for {targetImage}: {matched}")

            if matched:
                with self.lock:
                    self.matchedImages.append(targetImage)
                print(f"Match found: {targetImage}")
            
            return matched
        except Exception as e:
            print(f"Error processing image {targetImage}: {e}")
            return False

    async def process_batch(self, batch):
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as executor:
            tasks = [
                loop.run_in_executor(executor, self.imagesMatch, imgFile)
                for imgFile in batch
            ]
            await asyncio.gather(*tasks)

    async def run_batch(self, batch):
        await self.process_batch(batch)

    def searchAll(self):
        imgFiles = self.getTargetImageFilePaths()
        for i in range(len(imgFiles), 15):
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(self.imagesMatch, imgFile) for imgFile in imgFiles[i::15]]

            # Wait for all futures to complete
            concurrent.futures.wait(futures)

        print("All images processed.")
        return [future.result() for future in futures]

# Usage example:
matchMyFace = ImageMatcher("registeredPics\\103\\image.png", "D:\\Camera")
asyncio.run(matchMyFace.searchAll())
# asyncio.run(matchMyFace.searchAll(20))
# asyncio.run(matchMyFace.searchAll(20))
