import dlib
import cv2
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class FaceMatcher:
    def __init__(self, reference_image_path, images_directory, tolerance=0.6, max_workers=4):
        self.reference_image_path = reference_image_path
        self.images_directory = images_directory
        self.tolerance = tolerance
        self.max_workers = max_workers
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
        self.reference_encoding = self._load_reference_encoding()

    def _load_reference_encoding(self):
        print(f"Loading reference image from {self.reference_image_path}")
        image = cv2.imread(self.reference_image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        dets = self.detector(rgb_image, 1)
        if len(dets) == 0:
            raise ValueError("No faces found in the reference image!")
        shape = self.sp(rgb_image, dets[0])
        reference_encoding = np.array(self.facerec.compute_face_descriptor(rgb_image, shape))
        print("Reference image loaded and encoded successfully.")
        return reference_encoding

    def _load_image_file(self, file_path):
        print(f"Loading image from {file_path}")
        return cv2.imread(file_path)

    def _get_face_encodings(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        dets = self.detector(rgb_image, 1)
        encodings = []
        for det in dets:
            shape = self.sp(rgb_image, det)
            encoding = np.array(self.facerec.compute_face_descriptor(rgb_image, shape))
            encodings.append(encoding)
        return encodings

    def _is_face_match(self, face_encoding):
        distance = np.linalg.norm(self.reference_encoding - face_encoding)
        return distance <= self.tolerance

    def _process_image(self, image_path):
        try:
            image = self._load_image_file(image_path)
            face_encodings = self._get_face_encodings(image)
            for face_encoding in face_encodings:
                if self._is_face_match(face_encoding):
                    print(f"Match found in {image_path}")
                    return image_path
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
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
