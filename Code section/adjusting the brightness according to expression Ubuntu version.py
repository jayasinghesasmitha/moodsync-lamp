# Import required libraries
import cv2  # OpenCV for computer vision tasks
import numpy as np  # NumPy for numerical operations
import time  # For time-related functions
from deepface import DeepFace  # For facial expression analysis
import os  # For operating system interactions
import mediapipe as mp  # Google's MediaPipe for face mesh detection
from scipy.spatial import distance  # For calculating distances between points

def analyze_facial_movement(duration=20):
    """Main function to analyze facial movements and expressions over a specified duration."""
    
    print("Initializing facial movement analysis with MediaPipe...")
    
    # Initialize MediaPipe FaceMesh solution
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,  # For video stream
        max_num_faces=1,  # Only detect one face
        refine_landmarks=True,  # Use refined landmarks
        min_detection_confidence=0.5,  # Minimum confidence for detection
        min_tracking_confidence=0.5)  # Minimum confidence for tracking
    
    # Initialize webcam capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam")
        return None
    
    # Set webcam resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Initialize variables for tracking analysis
    start_time = time.time()
    frame_count = 0
    movement_data = []  # Stores movement metrics per frame
    expression_data = []  # Stores expression analysis results
    last_landmarks = None  # Stores previous frame's landmarks
    movement_intensity = 0  # Smoothed movement metric
    
    # Create directory to save analysis frames (using Linux path)
    os.makedirs("analysis_frames", exist_ok=True)
    
    print(f"Starting analysis for {duration} seconds...")
    print("Please move your face naturally in front of the camera.")
    
    # Main analysis loop - runs for specified duration
    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to capture frame")
            break
        
        frame_count += 1
        # Convert frame to RGB (MediaPipe requires RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe FaceMesh
        results = face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            # Get face landmarks for the first detected face
            face_landmarks = results.multi_face_landmarks[0]
            
            # Convert landmarks to NumPy array of (x,y) coordinates
            landmarks_np = np.array([(lm.x * frame.shape[1], lm.y * frame.shape[0]) 
                                for lm in face_landmarks.landmark])
            
            if last_landmarks is not None:
                # Calculate movement between current and previous landmarks
                movement = np.mean(np.sqrt(np.sum((landmarks_np - last_landmarks) ** 2, axis=1)))
                # Apply exponential smoothing to movement intensity
                movement_intensity = 0.9 * movement_intensity + 0.1 * movement
                
                # Extract specific facial features for expression analysis
                mouth_left = landmarks_np[61]  # Left mouth corner
                mouth_right = landmarks_np[291]  # Right mouth corner
                mouth_top = landmarks_np[13]  # Upper lip
                mouth_bottom = landmarks_np[14]  # Lower lip
                
                # Calculate mouth dimensions
                mouth_width = distance.euclidean(mouth_left, mouth_right)
                mouth_height = distance.euclidean(mouth_top, mouth_bottom)
                
                # Calculate average eyebrow positions
                left_eyebrow = np.mean(landmarks_np[65:70], axis=0)
                right_eyebrow = np.mean(landmarks_np[295:300], axis=0)
                
                # Store movement metrics
                movement_data.append({
                    'frame': frame_count,
                    'time': time.time() - start_time,
                    'movement': movement,
                    'mouth_width': mouth_width,
                    'mouth_height': mouth_height,
                    'eyebrow_pos': (left_eyebrow[1] + right_eyebrow[1]) / 2
                })
            
            last_landmarks = landmarks_np  # Update landmarks for next frame
            
            # Perform expression analysis every 5 frames (to reduce processing load)
            if frame_count % 5 == 0:
                try:
                    # Convert back to BGR for DeepFace
                    bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
                    
                    # Analyze facial expression using DeepFace
                    analysis = DeepFace.analyze(bgr_frame, actions=['emotion'], enforce_detection=False)
                    
                    # Handle case where DeepFace returns a list
                    if isinstance(analysis, list):
                        analysis = analysis[0]
                    
                    dominant_emotion = analysis['dominant_emotion']
                    
                    # Store expression data
                    expression_data.append({
                        'frame': frame_count,
                        'time': time.time() - start_time,
                        'emotion': dominant_emotion,
                        'emotion_scores': analysis['emotion']
                    })
                    
                    # Display dominant emotion on frame
                    cv2.putText(frame, f"Emotion: {dominant_emotion}", 
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                except Exception as e:
                    print(f"Expression analysis error: {str(e)}")
            
            # Draw facial landmarks on frame (first 50 landmarks)
            for landmark in face_landmarks.landmark[:50]:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
            
            # Display movement intensity on frame
            cv2.putText(frame, f"Movement: {movement_intensity:.2f}", 
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show the processed frame
        cv2.imshow('Facial Movement Analysis', frame)
        
        # Save frame every 30 frames for later analysis
        if frame_count % 30 == 0:
            cv2.imwrite(f"analysis_frames/frame_{frame_count}.jpg", frame)
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup resources
    cap.release()
    cv2.destroyAllWindows()
    
    print("\nAnalysis complete!")
    print(f"Processed {frame_count} frames in {duration} seconds.")
    
    # Process and summarize the collected data
    results = process_analysis_data(movement_data, expression_data, duration)
    
    return results

def process_analysis_data(movement_data, expression_data, duration):
    """Processes raw analysis data into summary statistics and conclusions."""
    
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
    
    # Calculate movement statistics
    movements = [m['movement'] for m in movement_data]
    results['average_movement'] = np.mean(movements)
    results['movement_variance'] = np.var(movements)
    
    # Classify movement pattern based on average movement
    if results['average_movement'] > 1.5:
        results['movement_pattern'] = "high"
    elif results['average_movement'] > 0.5:
        results['movement_pattern'] = "moderate"
    else:
        results['movement_pattern'] = "low"
    
    # Initialize expression tracking
    expression_counts = {}
    last_expression = None
    
    # Process expression data
    for expr in expression_data:
        emotion = expr['emotion']
        expression_counts[emotion] = expression_counts.get(emotion, 0) + 1
        
        # Count smile frames
        if emotion in ['happy', 'surprise']:
            results['smile_frames'] += 1
        # Count sad frames
        elif emotion in ['sad', 'fear', 'angry']:
            results['sad_frames'] += 1
            # Count potential crying frames (high sadness score)
            if expr['emotion_scores']['sad'] > 50:
                results['crying_frames'] += 1
        
        # Track expression changes
        if last_expression and last_expression != emotion:
            results['expression_changes'] += 1
        last_expression = emotion
    
    results['expressions'] = expression_counts
    
    # Generate conclusions based on analysis
    if results['smile_frames'] > len(expression_data) * 0.3:
        results['conclusions'].append("The user was smiling during the analysis.")
    
    if results['sad_frames'] > len(expression_data) * 0.3:
        results['conclusions'].append("The user showed sadness during the analysis.")
    
    if results['crying_frames'] > len(expression_data) * 0.1:
        results['conclusions'].append("The user may have been crying during the analysis.")
    
    if results['movement_pattern'] == "high":
        results['conclusions'].append("The user showed significant facial movement.")
    elif results['movement_pattern'] == "low":
        results['conclusions'].append("The user showed minimal facial movement.")
    
    return results

def display_results(results):
    """Displays the analysis results in a readable format."""
    
    if not results:
        print("No results to display.")
        return
    
    # Print summary statistics
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
    
    # Print conclusions
    print("\nConclusions:")
    if results['conclusions']:
        for conclusion in results['conclusions']:
            print(f"- {conclusion}")
    else:
        print("- No strong conclusions could be drawn from the analysis.")

if __name__ == "__main__":
    """Main execution block with error handling and dependency management."""
    
    try:
        # Check and install required packages if missing
        try:
            import mediapipe
        except ImportError:
            print("Installing MediaPipe...")
            import subprocess
            subprocess.run(["pip3", "install", "mediapipe"], check=True)
            import mediapipe
        
        try:
            import deepface
        except ImportError:
            print("Installing DeepFace...")
            import subprocess
            subprocess.run(["pip3", "install", "deepface"], check=True)
            import deepface
        
        # Run the analysis
        print("Starting analysis...")
        analysis_results = analyze_facial_movement(duration=20)
        
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
        # Handle any errors that occur during execution
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Keep console open until user presses Enter
        input("\nPress Enter to exit...")