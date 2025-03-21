from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt
import os
import time
import sys

def verify_with_webcam(reference_img_path):
    print(f"Python version: {sys.version}")
    print(f"OpenCV version: {cv2.__version__}")
    print(f"Reference image path: {reference_img_path}")
    
    # Check if reference image exists
    if not os.path.exists(reference_img_path):
        print(f"ERROR: Reference image does not exist at path: {reference_img_path}")
        return
    
    # Create a directory to save the webcam image if it doesn't exist
    save_dir = "webcam_captures"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"Created directory: {save_dir}")
    
    # Generate a filename with timestamp
    timestamp = int(time.time())
    webcam_img_path = os.path.join(save_dir, f"webcam_capture_{timestamp}.jpg")
    print(f"Will save webcam capture to: {webcam_img_path}")
    
    # Load the reference image
    print("Loading reference image...")
    reference_img = cv2.imread(reference_img_path)
    if reference_img is None:
        print(f"ERROR: Could not load reference image from {reference_img_path}")
        return
    print(f"Reference image loaded successfully. Shape: {reference_img.shape}")
    
    # Display the reference image
    try:
        plt.figure(figsize=(8, 6))
        plt.imshow(cv2.cvtColor(reference_img, cv2.COLOR_BGR2RGB))
        plt.title("Reference Image")
        plt.show()
        print("Reference image displayed")
    except Exception as e:
        print(f"WARNING: Could not display reference image: {str(e)}")
    
    # Initialize webcam
    print("Initializing webcam...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam")
        return
    
    print("Webcam initialized successfully. Capturing image in 5 seconds...")
    print("Please position yourself in front of the camera...")
    
    # Countdown timer (without showing the video feed)
    countdown = 5
    for i in range(countdown, 0, -1):
        print(f"Capturing in {i} seconds...")
        time.sleep(1)
    
    print("Capturing now!")
    
    # Capture image
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Failed to capture image from webcam")
        cap.release()
        return
    
    # Save the captured image
    cv2.imwrite(webcam_img_path, frame)
    print(f"Image captured and saved to {webcam_img_path}")
    
    # Release the webcam
    cap.release()
    print("Webcam released")
    
    # Check if the captured image exists
    if not os.path.exists(webcam_img_path):
        print(f"ERROR: Captured image not found at {webcam_img_path}")
        return
    
    # Display the captured image
    try:
        captured_img = cv2.imread(webcam_img_path)
        if captured_img is None:
            print(f"ERROR: Could not load captured image from {webcam_img_path}")
            return
            
        plt.figure(figsize=(8, 6))
        plt.imshow(cv2.cvtColor(captured_img, cv2.COLOR_BGR2RGB))
        plt.title("Captured Image")
        plt.show()
        print("Captured image displayed")
    except Exception as e:
        print(f"WARNING: Could not display captured image: {str(e)}")
    
    # Perform face verification
    try:
        print("Performing face verification...")
        result = DeepFace.verify(reference_img_path, webcam_img_path)
        
        print("\nVerification Result:")
        print(result)
        
        if result["verified"]:
            print("\n✅ MATCH: The person in the webcam is the same as the reference image.")
        else:
            print("\n❌ NO MATCH: The person in the webcam is different from the reference image.")
        
        return result
    
    except Exception as e:
        print(f"ERROR during verification: {str(e)}")
        return None

if __name__ == "__main__":
    try:
        # Path to your reference image
        reference_image_path = r"C:\Users\ASUS\Documents\GitHub\moodsync-lamp\resources\me.jpg"
        
        # Run the verification
        result = verify_with_webcam(reference_image_path)
        
        # Keep the console window open until user presses Enter
        input("\nPress Enter to exit...")
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        input("\nAn error occurred. Press Enter to exit...")


'''
Line-by-Line Explanation of the Face Verification Code
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt
import os
import time
import sys

These lines import the necessary libraries:

DeepFace: A facial recognition and analysis library
cv2: OpenCV for image processing and webcam access
matplotlib.pyplot: For displaying images
os: For file and directory operations
time: For adding delays and timestamps
sys: For accessing Python version information
def verify_with_webcam(reference_img_path):

This defines a function that takes a path to a reference image as input.

    print(f"Python version: {sys.version}")
    print(f"OpenCV version: {cv2.__version__}")
    print(f"Reference image path: {reference_img_path}")

These lines print diagnostic information about the Python version, OpenCV version, and the path to the reference image.

    # Check if reference image exists
    if not os.path.exists(reference_img_path):
        print(f"ERROR: Reference image does not exist at path: {reference_img_path}")
        return

This checks if the reference image file exists at the specified path. If not, it prints an error message and exits the function.

    # Create a directory to save the webcam image if it doesn't exist
    save_dir = "webcam_captures"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"Created directory: {save_dir}")

This creates a directory called "webcam_captures" to store the captured webcam images if it doesn't already exist.

    # Generate a filename with timestamp
    timestamp = int(time.time())
    webcam_img_path = os.path.join(save_dir, f"webcam_capture_{timestamp}.jpg")
    print(f"Will save webcam capture to: {webcam_img_path}")

This generates a unique filename for the webcam capture using the current Unix timestamp and constructs the full path where the image will be saved.

    # Load the reference image
    print("Loading reference image...")
    reference_img = cv2.imread(reference_img_path)
    if reference_img is None:
        print(f"ERROR: Could not load reference image from {reference_img_path}")
        return
    print(f"Reference image loaded successfully. Shape: {reference_img.shape}")

This loads the reference image using OpenCV and checks if it was loaded successfully. If not, it prints an error and exits. If successful, it prints the image dimensions.

    # Display the reference image
    try:
        plt.figure(figsize=(8, 6))
        plt.imshow(cv2.cvtColor(reference_img, cv2.COLOR_BGR2RGB))
        plt.title("Reference Image")
        plt.show()
        print("Reference image displayed")
    except Exception as e:
        print(f"WARNING: Could not display reference image: {str(e)}")

This attempts to display the reference image using matplotlib. It converts the image from BGR (OpenCV format) to RGB (matplotlib format). If there's an error displaying the image, it catches the exception and prints a warning.

    # Initialize webcam
    print("Initializing webcam...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam")
        return

This initializes the webcam using OpenCV. It attempts to open the default camera (index 0) and checks if it was opened successfully.

    print("Webcam initialized successfully. Capturing image in 5 seconds...")
    print("Please position yourself in front of the camera...")
    
    # Countdown timer (without showing the video feed)
    countdown = 5
    for i in range(countdown, 0, -1):
        print(f"Capturing in {i} seconds...")
        time.sleep(1)
    
    print("Capturing now!")

This creates a 5-second countdown before capturing the image, giving the user time to position themselves in front of the camera.

    # Capture image
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Failed to capture image from webcam")
        cap.release()
        return

This captures a single frame from the webcam. ret is a boolean indicating if the frame was successfully captured, and frame contains the image data. If capture fails, it prints an error, releases the webcam, and exits.

    # Save the captured image
    cv2.imwrite(webcam_img_path, frame)
    print(f"Image captured and saved to {webcam_img_path}")
    
    # Release the webcam
    cap.release()
    print("Webcam released")

This saves the captured frame to the file path generated earlier and releases the webcam resource.

    # Check if the captured image exists
    if not os.path.exists(webcam_img_path):
        print(f"ERROR: Captured image not found at {webcam_img_path}")
        return

This verifies that the image was actually saved to disk.

    # Display the captured image
    try:
        captured_img = cv2.imread(webcam_img_path)
        if captured_img is None:
            print(f"ERROR: Could not load captured image from {webcam_img_path}")
            return
            
        plt.figure(figsize=(8, 6))
        plt.imshow(cv2.cvtColor(captured_img, cv2.COLOR_BGR2RGB))
        plt.title("Captured Image")
        plt.show()
        print("Captured image displayed")
    except Exception as e:
        print(f"WARNING: Could not display captured image: {str(e)}")

This loads the saved webcam image and displays it using matplotlib, similar to how the reference image was displayed. It includes error handling in case the image can't be loaded or displayed.

    # Perform face verification
    try:
        print("Performing face verification...")
        result = DeepFace.verify(reference_img_path, webcam_img_path)
        
        print("\nVerification Result:")
        print(result)
        
        if result["verified"]:
            print("\n✅ MATCH: The person in the webcam is the same as the reference image.")
        else:
            print("\n❌ NO MATCH: The person in the webcam is different from the reference image.")
        
        return result
    
    except Exception as e:
        print(f"ERROR during verification: {str(e)}")
        return None

This uses the DeepFace library to compare the reference image with the webcam image. It prints the full result and a user-friendly message indicating whether the faces match. If there's an error during verification, it catches the exception and prints an error message.

if __name__ == "__main__":
    try:
        # Path to your reference image
        reference_image_path = r"C:\Users\ASUS\Documents\GitHub\moodsync-lamp\resources\me.jpg"
        
        # Run the verification
        result = verify_with_webcam(reference_image_path)
        
        # Keep the console window open until user presses Enter
        input("\nPress Enter to exit...")
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        input("\nAn error occurred. Press Enter to exit...")

This is the main execution block that runs when the script is executed directly (not imported):

It sets the path to the reference image
Calls the verify_with_webcam function with that path
Waits for the user to press Enter before exiting
Includes comprehensive error handling that catches any exceptions, prints the error message and stack trace, and keeps the console window open
The code is designed with extensive error handling and user feedback at each step, making it robust and user-friendly for face verification using a webcam.'
'''