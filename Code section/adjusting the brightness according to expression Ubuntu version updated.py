# Import required libraries
import cv2
import numpy as np
import time
from deepface import DeepFace
import os
import mediapipe as mp
from scipy.spatial import distance
import subprocess

# Global variables for brightness control
current_brightness = 70  # Track current brightness level

def set_brightness(level):
    """Set display brightness using xrandr (Linux)"""
    global current_brightness
    try:
        display = subprocess.check_output(
            ["xrandr --verbose | grep -i connected | grep -v disconnected | awk '{print $1}'"], 
            shell=True
        ).decode().strip()
        if display:
            brightness_level = max(0.3, min(1.0, level/100))  # Clamp between 0.3 and 1.0
            subprocess.run(f"xrandr --output {display} --brightness {brightness_level:.2f}", shell=True)
            current_brightness = level
    except Exception as e:
        print(f"Brightness control error: {str(e)}")

def smooth_brightness_transition(target):
    """Gradually adjust brightness to target level"""
    global current_brightness
    step_size = 2  # Percentage change per step
    delay = 0.01   # 10ms delay between steps
    
    while abs(current_brightness - target) > step_size:
        if current_brightness < target:
            new_level = min(current_brightness + step_size, target)
        else:
            new_level = max(current_brightness - step_size, target)
        
        set_brightness(new_level)
        time.sleep(delay)
    
    # Ensure we reach exact target
    set_brightness(target)

def analyze_facial_movement(duration=20):
    """Main function to analyze facial movements and expressions"""
    global current_brightness
    
    print("Initializing facial movement analysis with MediaPipe...")
    
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam")
        return None
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    start_time = time.time()
    frame_count = 0
    movement_data = []
    expression_data = []
    last_landmarks = None
    movement_intensity = 0
    
    os.makedirs("analysis_frames", exist_ok=True)
    
    # Initialize brightness
    smooth_brightness_transition(70)
    
    print(f"Starting analysis for {duration} seconds...")
    print("Please move your face naturally in front of the camera.")
    
    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to capture frame")
            break
        
        frame_count += 1
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            landmarks_np = np.array([(lm.x * frame.shape[1], lm.y * frame.shape[0]) 
                                for lm in face_landmarks.landmark])
            
            if last_landmarks is not None:
                movement = np.mean(np.sqrt(np.sum((landmarks_np - last_landmarks) ** 2, axis=1)))
                movement_intensity = 0.9 * movement_intensity + 0.1 * movement
                
                mouth_left = landmarks_np[61]
                mouth_right = landmarks_np[291]
                mouth_top = landmarks_np[13]
                mouth_bottom = landmarks_np[14]
                
                mouth_width = distance.euclidean(mouth_left, mouth_right)
                mouth_height = distance.euclidean(mouth_top, mouth_bottom)
                
                left_eyebrow = np.mean(landmarks_np[65:70], axis=0)
                right_eyebrow = np.mean(landmarks_np[295:300], axis=0)
                
                movement_data.append({
                    'frame': frame_count,
                    'time': time.time() - start_time,
                    'movement': movement,
                    'mouth_width': mouth_width,
                    'mouth_height': mouth_height,
                    'eyebrow_pos': (left_eyebrow[1] + right_eyebrow[1]) / 2
                })
            
            last_landmarks = landmarks_np
            
            if frame_count % 5 == 0:
                try:
                    bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
                    analysis = DeepFace.analyze(bgr_frame, actions=['emotion'], enforce_detection=False)
                    
                    if isinstance(analysis, list):
                        analysis = analysis[0]
                    
                    dominant_emotion = analysis['dominant_emotion']
                    
                    expression_data.append({
                        'frame': frame_count,
                        'time': time.time() - start_time,
                        'emotion': dominant_emotion,
                        'emotion_scores': analysis['emotion']
                    })
                    
                    cv2.putText(frame, f"Emotion: {dominant_emotion}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    # Adjust brightness based on emotion with smooth transitions
                    if dominant_emotion in ['happy', 'surprise']:
                        smooth_brightness_transition(100)  # Bright for positive emotions
                    elif dominant_emotion in ['sad', 'fear', 'angry']:
                        smooth_brightness_transition(30)   # Dim for negative emotions
                    else:
                        smooth_brightness_transition(70)   # Neutral brightness
                    
                except Exception as e:
                    print(f"Expression analysis error: {str(e)}")
            
            for landmark in face_landmarks.landmark[:50]:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
            
            cv2.putText(frame, f"Movement: {movement_intensity:.2f}", 
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Facial Movement Analysis', frame)
        
        if frame_count % 30 == 0:
            cv2.imwrite(f"analysis_frames/frame_{frame_count}.jpg", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    smooth_brightness_transition(70)  # Reset brightness to neutral
    
    print("\nAnalysis complete!")
    print(f"Processed {frame_count} frames in {duration} seconds.")
    
    results = process_analysis_data(movement_data, expression_data, duration)
    return results

def process_analysis_data(movement_data, expression_data, duration):
    """Processes raw analysis data into summary statistics"""
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
    
    if not movement_data or not expression_data:
        return results
    
    movements = [m['movement'] for m in movement_data]
    results['average_movement'] = np.mean(movements)
    results['movement_variance'] = np.var(movements)
    
    if results['average_movement'] > 1.5:
        results['movement_pattern'] = "high"
    elif results['average_movement'] > 0.5:
        results['movement_pattern'] = "moderate"
    else:
        results['movement_pattern'] = "low"
    
    expression_counts = {}
    last_expression = None
    
    for expr in expression_data:
        emotion = expr['emotion']
        expression_counts[emotion] = expression_counts.get(emotion, 0) + 1
        
        if emotion in ['happy', 'surprise']:
            results['smile_frames'] += 1
        elif emotion in ['sad', 'fear', 'angry']:
            results['sad_frames'] += 1
            if expr['emotion_scores']['sad'] > 50:
                results['crying_frames'] += 1
        
        if last_expression and last_expression != emotion:
            results['expression_changes'] += 1
        last_expression = emotion
    
    results['expressions'] = expression_counts
    
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
    """Displays the analysis results in a readable format"""
    if not results:
        print("No results to display.")
        return
    
    print("\n=== Facial Movement Analysis Results ===")
    print(f"Duration: {results['duration']} seconds")
    print(f"Total frames analyzed: {results['total_frames']}")
    print(f"Average facial movement: {results['average_movement']:.2f} (variance: {results['movement_variance']:.2f})")
    print(f"Movement pattern: {results['movement_pattern']}")
    
    print("\nExpression Distribution:")
    for emotion, count in results['expressions'].items():
        print(f"- {emotion}: {count} frames")
    
    print("\nSpecial Expressions:")
    print(f"Smiling frames: {results['smile_frames']}")
    print(f"Sad frames: {results['sad_frames']}")
    print(f"Possible crying frames: {results['crying_frames']}")
    
    print("\nConclusions:")
    if results['conclusions']:
        for conclusion in results['conclusions']:
            print(f"- {conclusion}")
    else:
        print("- No strong conclusions could be drawn from the analysis.")

if __name__ == "__main__":
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
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nPress Enter to exit...")