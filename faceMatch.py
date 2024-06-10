from typing import Generator, List
import face_recognition
import os, sys

class ImageMatcher:
    def __init__(self, sourceImagePath) -> None:
        self.sourceImagePath = sourceImagePath
        self.imageTypes = ["jpg", "png", "jpeg"]
        self.known_image = face_recognition.load_image_file(self.sourceImagePath)
        self.known_encoding = face_recognition.face_encodings(self.known_image, model="small")[0]


    def imagesMatch(self, targetImage: str) -> bool:
        unknown_image = face_recognition.load_image_file(targetImage)
        unknown_encoding = face_recognition.face_encodings(unknown_image, model = "small")
        if len(unknown_encoding) > 0:
            unknown_encoding = unknown_encoding[0]
        else:
            return False

        matched = any(face_recognition.compare_faces([self.known_encoding], unknown_encoding))

        return matched if matched else False

if __name__ == "__main__":
    if len(sys.argv):
        ref = sys.argv[1]
        target = sys.argv[2]
        print(f"{target} -> {ImageMatcher(ref).imagesMatch(target)}")