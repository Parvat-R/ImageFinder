import multiprocessing.popen_spawn_win32 as forking
import face_recognition
import os
from multiprocessing import Pool

# Load the reference image and encode the face
reference_image_path = 'registeredPics/103/image.png'
reference_image = face_recognition.load_image_file(reference_image_path)
reference_encoding = face_recognition.face_encodings(reference_image)[0]

# Initialize an empty list to store the matched images
matched_images = []

# Function to check if an image contains the reference face
def check_image(filename):
    image_path = os.path.join("D:\\Camera", filename)
    
    # Load the image and encode the faces
    image = face_recognition.load_image_file(image_path)
    image_encodings = face_recognition.face_encodings(image)
    
    # Compare the face encodings with the reference encoding
    for encoding in image_encodings:
        match = face_recognition.compare_faces([reference_encoding], encoding)
        if match[0]:
            return filename
    return None

# Get the list of image files in the directory
images_directory = 'D:\\Camera'
image_files = [filename for filename in os.listdir(images_directory) if filename.endswith(".jpg") or filename.endswith(".png")]

# Create a multiprocessing pool
pool = Pool()

# Run the check_image function in parallel for all image files
results = pool.map(check_image, image_files)

# Close the pool and wait for tasks to complete
pool.close()
pool.join()

# Filter out the matched images from the results
matched_images = [result for result in results if result is not None]

# Print the list of matched images
print("Matched images:")
for image in matched_images:
    print(os.path.join(images_directory, image))