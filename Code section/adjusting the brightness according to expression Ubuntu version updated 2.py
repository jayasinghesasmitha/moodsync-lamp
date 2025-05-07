# Import required libraries for image processing, numerical operations, and facial analysis
import cv2  # OpenCV for webcam capture and image processing
import numpy as np  # NumPy for numerical computations
import time  # Time module for timing analysis duration
from deepface import DeepFace  # DeepFace for emotion, age, and gender analysis
import os  # OS module for file and directory operations
import mediapipe as mp  # MediaPipe for facial landmark detection
from scipy.spatial import distance  # SciPy for calculating Euclidean distances
import subprocess  # Subprocess for system-level brightness control

# Global variable to track current brightness level
current_brightness = 70  # Initialize brightness at 70%

def set_brightness(level):
    """Set display brightness using xrandr (Linux)"""
    global current_brightness
    try:
        # Get the active display name using xrandr
        display = subprocess.check_output(
            ["xrandr --verbose | grep -i connected | grep -v disconnected | awk '{print $1}'"], 
            shell=True
        ).decode().strip()
        if display:
            # Clamp brightness between 0.3 (minimum) and 1.0 (maximum)
            brightness_level = max(0.3, min(1.0, level/100))
            # Execute xrandr command to set brightness
            subprocess.run(f"xrandr --output {display} --brightness {brightness_level:.2f}", shell=True)
            # Update global brightness variable
            current_brightness = level
    except Exception as e:
        # Print error if brightness control fails
        print(f"Brightness control error: {str(e)}")

def smooth_brightness_transition(target):
    """Gradually adjust brightness to target level for smooth transitions"""
    global current_brightness
    step_size = 1  # Smaller step size (1%) for smoother transitions
    delay = 0.005  # 5ms delay for faster but smooth adjustments
    
    # Continue adjusting until the difference is smaller than step size
    while abs(current_brightness - target) > step_size:
        if current_brightness < target:
            # Increment brightness if below target
            new_level = min(current_brightness + step_size, target)
        else:
            # Decrement brightness if above target
            new_level = max(current_brightness - step_size, target)
        
        # Apply new brightness level
        set_brightness(new_level)
        # Short delay to control transition speed
        time.sleep(delay)
    
    # Ensure exact target brightness is set
    set_brightness(target)

def analyze_facial_movement(duration=30):
    """Main function to analyze facial movements, expressions, and additional metrics"""
    global current_brightness
    
    # Print initialization message
    print("Initializing facial movement analysis with MediaPipe...")
    
    # Initialize MediaPipe Face Mesh for facial landmark detection
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,  # Continuous video mode
        max_num_faces=1,  # Detect only one face
        refine_landmarks=True,  # Include iris landmarks for better accuracy
        min_detection_confidence=0.6,  # Slightly higher confidence for robustness
        min_tracking_confidence=0.6  # Higher tracking confidence
    )
    
    # Open webcam (default camera, index 0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        # Exit if webcam cannot be opened
        print("ERROR: Could not open webcam")
        return None
    
    # Set webcam resolution for faster processing
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # Set higher frame rate for smoother capture
    cap.set(cv2.CAP_PROP_FPS, 60)
    
    # Initialize timing and counters
    start_time = time.time()
    frame_count = 0
    movement_data = []  # Store movement metrics
    expression_data = []  # Store expression metrics
    last_landmarks = None  # Track previous frame's landmarks
    movement_intensity = 0  # Smoothed movement intensity
    blink_count = 0  # Track eye blinks
    head_tilt_data = []  # Track head tilt angles
    
    # Create directory for saving frames
    os.makedirs("analysis_frames", exist_ok=True)
    
    # Set initial brightness to neutral
    smooth_brightness_transition(70)
    
    # Print analysis start message
    print(f"Starting analysis for {duration} seconds...")
    print("Please move your face naturally in front of the camera.")
    
    while (time.time() - start_time) < duration:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            # Exit if frame capture fails
            print("ERROR: Failed to capture frame")
            break
        
        # Increment frame counter
        frame_count += 1
        # Convert frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe Face Mesh
        results = face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            # Get landmarks for the detected face
            face_landmarks = results.multi_face_landmarks[0]
            # Convert landmarks to pixel coordinates
            landmarks_np = np.array([(lm.x * frame.shape[1], lm.y * frame.shape[0]) 
                                    for lm in face_landmarks.landmark])
            
            if last_landmarks is not None:
                # Calculate average movement (Euclidean distance) across landmarks
                movement = np.mean(np.sqrt(np.sum((landmarks_np - last_landmarks) ** 2, axis=1)))
                # Smooth movement intensity using exponential moving average
                movement_intensity = 0.9 * movement_intensity + 0.1 * movement
                
                # Extract key facial landmarks
                mouth_left = landmarks_np[61]  # Left corner of mouth
                mouth_right = landmarks_np[291]  # Right corner of mouth
                mouth_top = landmarks_np[13]  # Upper lip
                mouth_bottom = landmarks_np[14]  # Lower lip
                
                # Calculate mouth dimensions
                mouth_width = distance.euclidean(mouth_left, mouth_right)
                mouth_height = distance.euclidean(mouth_top, mouth_bottom)
                
                # Calculate eyebrow positions
                left_eyebrow = np.mean(landmarks_np[65:70], axis=0)
                right_eyebrow = np.mean(landmarks_np[295:300], axis=0)
                
                # Detect eye closure (blinking) using eye aspect ratio
                left_eye_top = landmarks_np[159]  # Top of left eye
                left_eye_bottom = landmarks_np[145]  # Bottom of left eye
                left_eye_left = landmarks_np[133]  # Left corner of left eye
                left_eye_right = landmarks_np[33]  # Right corner of left eye
                left_eye_height = distance.euclidean(left_eye_top, left_eye_bottom)
                left_eye_width = distance.euclidean(left_eye_left, left_eye_right)
                left_eye_ratio = left_eye_height / left_eye_width
                
                # Consider a blink if eye aspect ratio is low
                if left_eye_ratio < 0.2:
                    blink_count += 1
                
                # Calculate head tilt using nose bridge and chin
                nose_bridge = landmarks_np[1]  # Nose bridge
                chin = landmarks_np[152]  # Chin
                head_tilt = np.arctan2(chin[1] - nose_bridge[1], chin[0] - nose_bridge[0]) * 180 / np.pi
                
                # Store movement and facial metrics
                movement_data.append({
                    'frame': frame_count,
                    'time': time.time() - start_time,
                    'movement': movement,
                    'mouth_width': mouth_width,
                    'mouth_height': mouth_height,
                    'eyebrow_pos': (left_eyebrow[1] + right_eyebrow[1]) / 2,
                    'head_tilt': head_tilt
                })
            
            # Update last landmarks for next iteration
            last_landmarks = landmarks_np
            
            # Perform emotion analysis every 3 frames for better responsiveness
            if frame_count % 3 == 0:
                try:
                    # Convert frame back to BGR for DeepFace
                    bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
                    # Analyze emotions, age, and gender
                    analysis = DeepFace.analyze(
                        bgr_frame, 
                        actions=['emotion', 'age', 'gender'], 
                        enforce_detection=False
                    )
                    
                    # Handle case where analysis returns a list
                    if isinstance(analysis, list):
                        analysis = analysis[0]
                    
                    # Extract dominant emotion
                    dominant_emotion = analysis['dominant_emotion']
                    
                    # Store expression data
                    expression_data.append({
                        'frame': frame_count,
                        'time': time.time() - start_time,
                        'emotion': dominant_emotion,
                        'emotion_scores': analysis['emotion'],
                        'age': analysis['age'],
                        'gender': analysis['gender']
                    })
                    
                    # Display emotion on frame
                    cv2.putText(frame, f"Emotion: {dominant_emotion}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    # Display age and gender
                    cv2.putText(frame, f"Age: {analysis['age']}", 
                               (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, f"Gender: {analysis['gender']}", 
                               (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    # Adjust brightness based on emotion
                    if dominant_emotion in ['happy', 'surprise']:
                        smooth_brightness_transition(100)  # Bright for positive emotions
                    elif dominant_emotion in ['sad', 'fear', 'angry', 'disgust']:
                        smooth_brightness_transition(30)   # Dim for negative emotions
                    else:
                        smooth_brightness_transition(70)   # Neutral brightness
                    
                except Exception as e:
                    # Print error if expression analysis fails
                    print(f"Expression analysis error: {str(e)}")
            
            # Draw facial landmarks on frame (first 50 for simplicity)
            for landmark in face_landmarks.landmark[:50]:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
            
            # Display movement intensity and blink count
            cv2.putText(frame, f"Movement: {movement_intensity:.2f}", 
                        (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Blinks: {blink_count}", 
                        (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display the frame
        cv2.imshow('Facial Movement Analysis', frame)
        
        # Save frame every 20 frames (reduced from 30 for more captures)
        if frame_count % 20 == 0:
            cv2.imwrite(f"analysis_frames/frame_{frame_count}.jpg", frame)
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release webcam and close windows
    cap.release()
    cv2.destroyAllWindows()
    # Reset brightness to neutral
    smooth_brightness_transition(70)
    
    # Print completion message
    print("\nAnalysis complete!")
    print(f"Processed {frame_count} frames in {duration} seconds.")
    
    # Process and return results
    results = process_analysis_data(movement_data, expression_data, duration, blink_count)
    return results

def process_analysis_data(movement_data, expression_data, duration, blink_count):
    """Processes raw analysis data into summary statistics"""
    results = {
        'total_frames': len(movement_data),
        'duration': duration,
        'average_movement': 0,
        'movement_variance': 0,
        'average_head_tilt': 0,
        'expressions': {},
        'expression_changes': 0,
        'smile_frames': 0,
        'sad_frames': 0,
        'crying_frames': 0,
        'blink_count': blink_count,
        'movement_pattern': None,
        'conclusions': []
    }
    
    # Return empty results if no data
    if not movement_data or not expression_data:
        return results
    
    # Calculate movement statistics
    movements = [m['movement'] for m in movement_data]
    results['average_movement'] = np.mean(movements)
    results['movement_variance'] = np.var(movements)
    
    # Calculate average head tilt
    head_tilts = [m['head_tilt'] for m in movement_data]
    results['average_head_tilt'] = np.mean(head_tilts)
    
    # Determine movement pattern based on normalized thresholds
    if results['average_movement'] > 2.0:
        results['movement_pattern'] = "high"
    elif results['average_movement'] > 0.7:
        results['movement_pattern'] = "moderate"
    else:
        results['movement_pattern'] = "low"
    
    # Process expression data
    expression_counts = {}
    last_expression = None
    
    for expr in expression_data:
        emotion = expr['emotion']
        # Count occurrences of each emotion
        expression_counts[emotion] = expression_counts.get(emotion, 0) + 1
        
        # Categorize special expressions
        if emotion in ['happy', 'surprise']:
            results['smile_frames'] += 1
        elif emotion in ['sad', 'fear', 'angry', 'disgust']:
            results['sad_frames'] += 1
            if expr['emotion_scores']['sad'] > 60:  # Higher threshold for crying
                results['crying_frames'] += 1
        
        # Count expression changes
        if last_expression and last_expression != emotion:
            results['expression_changes'] += 1
        last_expression = emotion
    
    results['expressions'] = expression_counts
    
    # Generate conclusions based on analysis
    if results['smile_frames'] > len(expression_data) * 0.3:
        results['conclusions'].append("The user was smiling frequently during the analysis.")
    
    if results['sad_frames'] > len(expression_data) * 0.3:
        results['conclusions'].append("The user showed sadness or negative emotions frequently.")
    
    if results['crying_frames'] > len(expression_data) * 0.1:
        results['conclusions'].append("The user may have been crying during the analysis.")
    
    if results['blink_count'] > duration * 0.3:
        results['conclusions'].append("The user blinked frequently, possibly indicating fatigue or stress.")
    
    if results['movement_pattern'] == "high":
        results['conclusions'].append("The user showed significant facial movement.")
    elif results['movement_pattern'] == "low":
        results['conclusions'].append("The user showed minimal facial movement.")
    
    if abs(results['average_head_tilt']) > 15:
        results['conclusions'].append("The user exhibited noticeable head tilting.")
    
    return results

def display_results(results):
    """Displays the analysis results in a readable format"""
    if not results:
        print("No results to display.")
        return
    
    # Print detailed results
    print("\n=== Facial Movement Analysis Results ===")
    print(f"Duration: {results['duration']} seconds")
    print(f"Total frames analyzed: {results['total_frames']}")
    print(f"Average facial movement: {results['average_movement']:.2f} (variance: {results['movement_variance']:.2f})")
    print(f"Average head tilt: {results['average_head_tilt']:.2f} degrees")
    print(f"Movement pattern: {results['movement_pattern']}")
    print(f"Total blinks detected: {results['blink_count']}")
    
    print("\nExpression Distribution:")
    for emotion, count in results['expressions'].items():
        print(f"- {emotion}: {count} frames")
    
    print("\nSpecial Expressions:")
    print(f"Smiling frames: {results['smile_frames']}")
    print(f"Sad/Negative frames: {results['sad_frames']}")
    print(f"Possible crying frames: {results['crying_frames']}")
    
    print("\nConclusions:")
    if results['conclusions']:
        for conclusion in results['conclusions']:
            print(f"- {conclusion}")
    else:
        print("- No strong conclusions could be drawn from the analysis.")

if __name__ == "__main__":
    try:
        # Check and install MediaPipe if missing
        try:
            import mediapipe
        except ImportError:
            print("Installing MediaPipe...")
            subprocess.run(["pip3", "install", "mediapipe"], check=True)
            import mediapipe
        
        # Check and install DeepFace if missing
        try:
            import deepface
        except ImportError:
            print("Installing DeepFace...")
            subprocess.run(["pip3", "install", "deepface"], check=True)
            import deepface
        
        # Run analysis for 30 seconds (increased duration)
        print("Starting analysis...")
        analysis_results = analyze_facial_movement(duration=30)
        
        # Display results
        display_results(analysis_results)
        
        # Save results to file
        with open("analysis_results.txt", "w") as f:
            f.write("Facial Movement Analysis Results\n")
            f.write("="*40 + "\n")
            for key, value in analysis_results.items():
                if key == 'conclusions':
                    f.write("\nConclusions:\n")
                    for conclusion in value:
                        f.write(f"- {conclusion}\n")
                else:
                    f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        
        print("\nResults saved to 'analysis_results.txt'")
        
    except Exception as e:
        # Print detailed error with traceback
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Wait for user input to exit
        input("\nPress Enter to exit...")