# Import necessary libraries
import cv2  # OpenCV for computer vision tasks
import numpy as np  # Numerical computing library
import time  # For time-related functions
from deepface import DeepFace  # For facial emotion analysis
import os  # For operating system related functions
import mediapipe as mp  # Google's MediaPipe for face mesh detection
from scipy.spatial import distance  # For calculating distances between points
import math  # Math operations (though not directly used in current implementation)

def analyze_facial_movement(duration=10):
    """
    Analyze facial movements and expressions for a specified duration using MediaPipe.
    
    Args:
        duration (int): Duration of analysis in seconds (default: 10)
    
    Returns:
        dict: Analysis results including movement metrics and detected expressions
    """
    
    print("Initializing facial movement analysis with MediaPipe...")
    
    # Initialize MediaPipe Face Mesh solution
    # FaceMesh provides 468 facial landmarks for detailed face tracking
    mp_face_mesh = mp.solutions.face_mesh
    
    # Create FaceMesh instance with configuration parameters:
    # static_image_mode=False - better for video streams
    # max_num_faces=1 - we only track one face
    # refine_landmarks=True - provides additional landmarks around eyes and lips
    # min_detection_confidence - threshold for face detection
    # min_tracking_confidence - threshold for landmark tracking
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)
    
    # Initialize webcam capture
    # 0 refers to the default webcam
    cap = cv2.VideoCapture(0)
    
    # Check if webcam was successfully opened
    if not cap.isOpened():
        print("ERROR: Could not open webcam")
        return None
    
    # Set webcam resolution to 640x480 for consistent processing
    # Adjust these values based on your webcam's capabilities
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Variables for tracking and analysis:
    start_time = time.time()  # Record when analysis started
    frame_count = 0  # Count total frames processed
    movement_data = []  # Store movement metrics per frame
    expression_data = []  # Store emotion analysis results
    last_landmarks = None  # Store previous frame's landmarks for movement calculation
    movement_intensity = 0  # Smoothed movement metric
    
    # Create directory to save sample frames if it doesn't exist
    os.makedirs("analysis_frames", exist_ok=True)
    
    print(f"Starting analysis for {duration} seconds...")
    print("Please move your face naturally in front of the camera.")
    
    # Main analysis loop - runs for specified duration
    while (time.time() - start_time) < duration:
        # Read a frame from the webcam
        # ret indicates if frame was successfully captured
        # frame contains the image data
        ret, frame = cap.read()
        
        # If frame capture failed, break the loop
        if not ret:
            print("ERROR: Failed to capture frame")
            break
        
        frame_count += 1  # Increment frame counter
        
        # Convert frame from BGR (OpenCV default) to RGB (MediaPipe expects RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame with MediaPipe Face Mesh
        results = face_mesh.process(rgb_frame)
        
        # Check if any faces were detected
        if results.multi_face_landmarks:
            # Get the landmarks for the primary face (we only track one face)
            face_landmarks = results.multi_face_landmarks[0]
            
            # Convert landmarks to numpy array for easier calculations
            # Each landmark has x,y coordinates normalized to [0,1]
            # We multiply by frame dimensions to get pixel coordinates
            landmarks_np = np.array([(lm.x * frame.shape[1], lm.y * frame.shape[0]) 
                                    for lm in face_landmarks.landmark])
            
            # Calculate movement metrics if we have landmarks from previous frame
            if last_landmarks is not None:
                # Calculate movement as average Euclidean distance between corresponding landmarks
                movement = np.mean(np.sqrt(np.sum((landmarks_np - last_landmarks) ** 2, axis=1)))
                
                # Apply exponential smoothing to movement intensity
                # This helps reduce jitter in the measurements
                movement_intensity = 0.9 * movement_intensity + 0.1 * movement
                
                # Calculate specific facial features using key landmarks:
                # Mouth width (distance between mouth corners)
                mouth_left = landmarks_np[61]  # Left corner of mouth
                mouth_right = landmarks_np[291]  # Right corner of mouth
                mouth_width = distance.euclidean(mouth_left, mouth_right)
                
                # Mouth height (distance between upper and lower lip)
                mouth_top = landmarks_np[13]  # Top of upper lip
                mouth_bottom = landmarks_np[14]  # Bottom of lower lip
                mouth_height = distance.euclidean(mouth_top, mouth_bottom)
                
                # Eyebrow position (average y-coordinate of eyebrow points)
                left_eyebrow = np.mean(landmarks_np[65:70], axis=0)
                right_eyebrow = np.mean(landmarks_np[295:300], axis=0)
                
                # Store movement metrics for this frame
                movement_data.append({
                    'frame': frame_count,
                    'time': time.time() - start_time,
                    'movement': movement,
                    'mouth_width': mouth_width,
                    'mouth_height': mouth_height,
                    'eyebrow_pos': (left_eyebrow[1] + right_eyebrow[1]) / 2
                })
            
            # Store current landmarks for next frame's movement calculation
            last_landmarks = landmarks_np
            
            # Analyze facial expression using DeepFace every 5 frames
            # We don't analyze every frame to reduce processing load
            if frame_count % 5 == 0:
                try:
                    # Convert back to BGR format for DeepFace (which expects BGR)
                    bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
                    
                    # Analyze facial expression using DeepFace
                    # We only request emotion analysis to reduce processing
                    analysis = DeepFace.analyze(bgr_frame, actions=['emotion'], enforce_detection=False)
                    
                    # DeepFace returns a list if multiple faces are detected
                    # We just take the first face's analysis
                    if isinstance(analysis, list):
                        analysis = analysis[0]
                    
                    # Store expression analysis results
                    expression_data.append({
                        'frame': frame_count,
                        'time': time.time() - start_time,
                        'emotion': analysis['dominant_emotion'],
                        'emotion_scores': analysis['emotion']
                    })
                    
                    # Display the dominant emotion on the frame
                    cv2.putText(frame, f"Emotion: {analysis['dominant_emotion']}", 
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                except Exception as e:
                    print(f"Expression analysis error: {str(e)}")
            
            # Draw facial landmarks on the frame for visualization
            # We only draw the first 50 landmarks for performance
            for landmark in face_landmarks.landmark[:50]:
                # Convert normalized coordinates to pixel coordinates
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
            
            # Display the current movement intensity on the frame
            cv2.putText(frame, f"Movement: {movement_intensity:.2f}", 
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display the processed frame in a window
        cv2.imshow('Facial Movement Analysis', frame)
        
        # Save sample frame every second (assuming ~30fps)
        if frame_count % 30 == 0:
            cv2.imwrite(f"Code section/analysis_frames/frame_{frame_count}.jpg", frame)
        
        # Check for 'q' key press to exit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources when analysis is complete
    cap.release()  # Release webcam
    cv2.destroyAllWindows()  # Close all OpenCV windows
    
    # Print completion message
    print("\nAnalysis complete!")
    print(f"Processed {frame_count} frames in {duration} seconds.")
    
    # Process the collected data into summary metrics
    results = process_analysis_data(movement_data, expression_data, duration)
    
    return results

def process_analysis_data(movement_data, expression_data, duration):
    """
    Process the collected movement and expression data to generate insights.
    
    Args:
        movement_data (list): List of movement metrics per frame
        expression_data (list): List of expression analysis results
        duration (int): Total duration of analysis
    
    Returns:
        dict: Processed results with insights
    """
    # Initialize results dictionary with default values
    results = {
        'total_frames': len(movement_data),
        'duration': duration,
        'average_movement': 0,
        'movement_variance': 0,
        'expressions': {},
        'expression_changes': 0,
        'smile_frames': 0,
        'sad_frames': 0,
        'crying_frames': 0,
        'movement_pattern': None,
        'conclusions': []
    }
    
    # Return empty results if no data was collected
    if not movement_data or not expression_data:
        return results
    
    # Calculate basic movement statistics
    movements = [m['movement'] for m in movement_data]  # Extract all movement values
    results['average_movement'] = np.mean(movements)  # Calculate mean movement
    results['movement_variance'] = np.var(movements)  # Calculate variance
    
    # Classify movement pattern based on average movement
    if results['average_movement'] > 1.5:
        results['movement_pattern'] = "high"
    elif results['average_movement'] > 0.5:
        results['movement_pattern'] = "moderate"
    else:
        results['movement_pattern'] = "low"
    
    # Process expression data
    expression_counts = {}  # Dictionary to count each emotion occurrence
    last_expression = None  # Track previous emotion for change detection
    
    for expr in expression_data:
        emotion = expr['emotion']
        
        # Update count for this emotion
        expression_counts[emotion] = expression_counts.get(emotion, 0) + 1
        
        # Categorize frames for special expressions
        if emotion in ['happy', 'surprise']:
            results['smile_frames'] += 1
        elif emotion in ['sad', 'fear', 'angry']:
            results['sad_frames'] += 1
            # Check for possible crying (high sadness score)
            if expr['emotion_scores']['sad'] > 50:
                results['crying_frames'] += 1
        
        # Count expression changes
        if last_expression and last_expression != emotion:
            results['expression_changes'] += 1
        last_expression = emotion
    
    results['expressions'] = expression_counts
    
    # Generate conclusions based on the analysis
    # Smiling conclusion
    if results['smile_frames'] > len(expression_data) * 0.3:
        results['conclusions'].append("The user was smiling during the analysis.")
    
    # Sadness conclusion
    if results['sad_frames'] > len(expression_data) * 0.3:
        results['conclusions'].append("The user showed sadness during the analysis.")
    
    # Crying conclusion
    if results['crying_frames'] > len(expression_data) * 0.1:
        results['conclusions'].append("The user may have been crying during the analysis.")
    
    # Movement pattern conclusions
    if results['movement_pattern'] == "high":
        results['conclusions'].append("The user showed significant facial movement.")
    elif results['movement_pattern'] == "low":
        results['conclusions'].append("The user showed minimal facial movement.")
    
    return results

def display_results(results):
    """Display the analysis results in a readable format."""
    if not results:
        print("No results to display.")
        return
    
    # Print summary header
    print("\n=== Facial Movement Analysis Results ===")
    print(f"Duration: {results['duration']} seconds")
    print(f"Total frames analyzed: {results['total_frames']}")
    print(f"Average facial movement: {results['average_movement']:.2f} (variance: {results['movement_variance']:.2f})")
    print(f"Movement pattern: {results['movement_pattern']}")
    
    # Print expression distribution
    print("\nExpression Distribution:")
    for emotion, count in results['expressions'].items():
        print(f"- {emotion}: {count} frames")
    
    # Print special expression counts
    print("\nSpecial Expressions:")
    print(f"Smiling frames: {results['smile_frames']}")
    print(f"Sad frames: {results['sad_frames']}")
    print(f"Possible crying frames: {results['crying_frames']}")
    
    # Print generated conclusions
    print("\nConclusions:")
    if results['conclusions']:
        for conclusion in results['conclusions']:
            print(f"- {conclusion}")
    else:
        print("- No strong conclusions could be drawn from the analysis.")

if __name__ == "__main__":
    try:
        # Check for and install required packages if missing
        try:
            import mediapipe
        except ImportError:
            print("Installing MediaPipe...")
            import subprocess
            subprocess.run(["pip", "install", "mediapipe"], check=True)
            import mediapipe
        
        try:
            import deepface
        except ImportError:
            print("Installing DeepFace...")
            import subprocess
            subprocess.run(["pip", "install", "deepface"], check=True)
            import deepface
        
        # Run the analysis for 10 seconds
        print("Starting analysis...")
        analysis_results = analyze_facial_movement(duration=10)
        
        # Display results in console
        display_results(analysis_results)
        
        # Save results to a text file
        with open("Code section/analysis_results.txt", "w") as f:
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
        # Print any errors that occur
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Keep console open until user presses Enter
        input("\nPress Enter to exit...")