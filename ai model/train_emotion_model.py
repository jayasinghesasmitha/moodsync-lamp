# Import required libraries for image processing, model building, and data handling
import os  # For file and directory operations
import cv2  # For image loading and preprocessing
import numpy as np  # For numerical computations
import tensorflow as tf  # For building and training the CNN
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # For data augmentation
from tensorflow.keras.models import Sequential  # For sequential model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout  # For CNN layers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint  # For training callbacks
import shutil  # For file moving
from sklearn.model_selection import train_test_split  # For splitting dataset
import json  # For loading analysis results

# Define emotion classes based on DeepFace output
EMOTIONS = ['happy', 'sad', 'angry', 'surprise', 'fear', 'neutral', 'disgust']
IMG_SIZE = 224  # Target image size for resizing
BATCH_SIZE = 32  # Batch size for training
DATA_DIR = "emotion_dataset"  # Directory to store organized dataset

def load_analysis_results(results_file="analysis_results.txt"):
    """Load frame-to-emotion mappings from analysis_results.txt or expression_data"""
    # Placeholder for frame-to-emotion mapping
    # In practice, parse analysis_results.txt or re-run analyze_facial_movement to get expression_data
    frame_emotions = {}
    
    # Example: Assume expression_data is available or parsed from results
    # This is a simplified mock-up; you may need to parse the actual file
    # For demonstration, assume frames are mapped to emotions based on frame numbers
    try:
        with open(results_file, 'r') as f:
            lines = f.readlines()
            # Parse expressions from the file (adjust based on actual format)
            for line in lines:
                if line.startswith("Expressions:"):
                    expressions_str = line.split(":")[1].strip()
                    expressions = eval(expressions_str)  # Convert string dict to dict
                    for emotion, count in expressions.items():
                        # Distribute frames evenly (simplified assumption)
                        for i in range(count):
                            frame_num = len(frame_emotions) * 10  # Approximate frame number
                            frame_emotions[f"frame_{frame_num}.jpg"] = emotion
    except Exception as e:
        print(f"Error loading analysis results: {e}")
        # Fallback: Mock data for demonstration
        for i in range(1000):  # Assume 1000 frames
            frame_num = i * 10
            emotion = EMOTIONS[i % len(EMOTIONS)]  # Cycle through emotions
            frame_emotions[f"frame_{frame_num}.jpg"] = emotion
    
    return frame_emotions

def organize_dataset(frame_emotions, source_dir="analysis_frames"):
    """Organize frames into subdirectories based on emotions"""
    # Create dataset directory
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Create subdirectories for each emotion
    for emotion in EMOTIONS:
        os.makedirs(os.path.join(DATA_DIR, emotion), exist_ok=True)
    
    # Move frames to corresponding emotion directories
    for frame_name, emotion in frame_emotions.items():
        src_path = os.path.join(source_dir, frame_name)
        dst_path = os.path.join(DATA_DIR, emotion, frame_name)
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)  # Copy to preserve original
            print(f"Copied {frame_name} to {emotion} folder")
        else:
            print(f"Frame {frame_name} not found in {source_dir}")

def create_data_generators():
    """Create data generators for training, validation, and testing with augmentation"""
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,  # Normalize pixel values to [0, 1]
        rotation_range=20,  # Random rotation
        width_shift_range=0.2,  # Horizontal shift
        height_shift_range=0.2,  # Vertical shift
        horizontal_flip=True,  # Random horizontal flip
        fill_mode='nearest'  # Fill missing pixels
    )
    
    # No augmentation for validation and test, only normalization
    valid_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load images from directories
    train_generator = train_datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    valid_generator = valid_datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    return train_generator, valid_generator

def build_cnn_model():
    """Build a convolutional neural network for emotion classification"""
    model = Sequential([
        # First convolutional block
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        MaxPooling2D((2, 2)),
        # Second convolutional block
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        # Third convolutional block
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        # Flatten and dense layers
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),  # Prevent overfitting
        Dense(len(EMOTIONS), activation='softmax')  # Output layer for emotion classes
    ])
    
    # Compile the model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model(train_generator, valid_generator):
    """Train the CNN model with early stopping and model checkpointing"""
    model = build_cnn_model()
    
    # Define callbacks
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )
    checkpoint = ModelCheckpoint(
        'emotion_model_best.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max'
    )
    
    # Train the model
    history = model.fit(
        train_generator,
        epochs=50,  # Maximum epochs
        validation_data=valid_generator,
        callbacks=[early_stopping, checkpoint]
    )
    
    # Save the final model
    model.save('emotion_model_final.h5')
    
    return model, history

def evaluate_model(model, test_generator):
    """Evaluate the model on the test set"""
    test_loss, test_accuracy = model.evaluate(test_generator)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")

def main():
    """Main function to orchestrate dataset preparation and model training"""
    try:
        # Step 1: Load frame-to-emotion mappings
        print("Loading analysis results...")
        frame_emotions = load_analysis_results()
        
        # Step 2: Organize dataset into emotion subdirectories
        print("Organizing dataset...")
        organize_dataset(frame_emotions)
        
        # Step 3: Create data generators
        print("Creating data generators...")
        # Split dataset: 80% training, 20% validation (test set can be added if needed)
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            validation_split=0.2  # 20% for validation
        )
        
        train_generator = train_datagen.flow_from_directory(
            DATA_DIR,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        valid_generator = train_datagen.flow_from_directory(
            DATA_DIR,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        
        # Step 4: Train the model
        print("Training the model...")
        model, history = train_model(train_generator, valid_generator)
        
        # Step 5: Evaluate the model (using validation as test for simplicity)
        print("Evaluating the model...")
        evaluate_model(model, valid_generator)
        
        # Save training history
        with open('training_history.json', 'w') as f:
            json.dump(history.history, f)
        
        print("Model training complete. Models saved as 'emotion_model_best.h5' and 'emotion_model_final.h5'")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Install required dependencies if missing
    try:
        import tensorflow
    except ImportError:
        print("Installing TensorFlow...")
        import subprocess
        subprocess.run(["pip3", "install", "tensorflow"], check=True)
        import tensorflow
    
    # Run the main function
    main()