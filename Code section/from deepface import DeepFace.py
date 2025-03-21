from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt

def verify(img1_path, img2_path):
    # Read images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    # Check if images were loaded successfully
    if img1 is None or img2 is None:
        print("Error: Could not load one or both images.")
        return
    
    # Display first image (convert BGR to RGB for matplotlib)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img1[:, :, ::-1])
    plt.title("Image 1")
    plt.axis('off')
    
    # Display second image
    plt.subplot(1, 2, 2)
    plt.imshow(img2[:, :, ::-1])
    plt.title("Image 2")
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    # Perform face verification
    try:
        output = DeepFace.verify(img1_path, img2_path)
        print("Verification Result:")
        print(output)
        
        verification = output['verified']
        
        if verification:
            print('✅ Verification Result: They are the same person')
        else:
            print('❌ Verification Result: They are not the same person')
        
        # Print confidence score
        print(f"Distance: {output['distance']:.4f}")
        threshold = 0.4
        confidence_percentage = max(0, min(100, (1 - (output['distance'] / threshold)) * 100))
        print(f"Confidence percentage: {confidence_percentage:.2f}%")
        return verification
        
    except Exception as e:
        print(f"Error during verification: {str(e)}")
        return None

if __name__ == "__main__":
    # Hardcoded image paths
    img1_path = r"C:\Users\ASUS\Documents\GitHub\moodsync-lamp\resources\me.jpg"
    img2_path = r"C:\Users\ASUS\Downloads\me.jpg"
    
    # Call the verify function with the provided image paths
    verify(img1_path, img2_path)

