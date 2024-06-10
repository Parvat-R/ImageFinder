import face_recognition
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class FaceMatcher:
    def __init__(self, reference_image_path, images_directory, tolerance=0.6, max_workers=4):
        self.reference_image_path = reference_image_path
        self.images_directory = images_directory
        self.tolerance = tolerance
        self.max_workers = max_workers
        self.reference_encoding = self._load_reference_encoding()

    def _load_reference_encoding(self):
        reference_image = face_recognition.load_image_file(self.reference_image_path)
        reference_encodings = face_recognition.face_encodings(reference_image)
        if not reference_encodings:
            raise ValueError("No faces found in the reference image!")
        return reference_encodings[0]

    def _load_image_file(self, file_path):
        return face_recognition.load_image_file(file_path)

    def _get_face_encodings(self, image):
        return face_recognition.face_encodings(image)

    def _is_face_match(self, face_encoding):
        return face_recognition.compare_faces([self.reference_encoding], face_encoding, tolerance=self.tolerance)[0]

    def _process_image(self, image_path):
        image = self._load_image_file(image_path)
        face_encodings = self._get_face_encodings(image)
        for face_encoding in face_encodings:
            if self._is_face_match(face_encoding):
                return image_path
        return None

    def find_matching_images(self):
        image_files = [os.path.join(self.images_directory, filename)
                       for filename in os.listdir(self.images_directory)
                       if filename.lower().endswith(('png', 'jpg', 'jpeg'))]

        matching_images = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._process_image, image_path): image_path for image_path in image_files}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    matching_images.append(result)
        return matching_images

# Example usage
reference_image_path = 'registeredPics/103/image.png'
images_directory = 'D:\\Camera'

matcher = FaceMatcher(reference_image_path, images_directory)
matching_images = matcher.find_matching_images()

print("Matching images:")
for image_path in matching_images:
    print(image_path)
