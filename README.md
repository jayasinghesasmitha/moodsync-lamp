# 🌈 Mood-Based Smart Lighting System

Welcome to the repository for our **IoT Mood-Based Lighting System**, a project that blends facial emotion recognition with intelligent lighting control to enhance mental well-being. By analyzing facial expressions, our system dynamically adjusts the brightness of a lamp to reflect and respond to the user's mood.

## 😃 Project Concept

The system uses facial emotion detection to determine the user's mood and modifies the light intensity.
For examples:
- **Happy** → Neutral brightness
- **Sad** → Increased brightness to uplift mood
- **Other moods** → Adaptive responses based on emotional context

This concept is inspired by research on how lighting affects psychological states:
- [Light and mental health – The Conversation](https://theconversation.com/how-light-can-shift-your-mood-and-mental-health-231282)
- [Lighting and mood – Illuminated Integration](https://illuminated-integration.com/blog/how-lighting-affects-mood/)

## 🧠 Tech Stack

### Software
- **Node.js**: Backend logic and facial emotion processing
- **Firebase**: Real-time database and cloud storage
- **MQTT**: Lightweight messaging protocol for device communication

### Hardware
- **ESP32**: Microcontroller for controlling the lamp
- **Camera Module**: Captures facial expressions
- **Smart Lamp**: Adjustable brightness based on mood

## 🔁 System Workflow

1. Camera captures user's face
2. Node.js app analyzes mood using facial recognition
3. Mood data is stored in Firebase
4. ESP32 receives mood data via MQTT
5. Lamp brightness is adjusted accordingly

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/mood-lighting-iot.git
   ```
2. Set up Firebase and configure credentials.
3. Run the Node.js app to start mood detection.
4. Flash ESP32 with the provided code.
5. Connect all components and test the system.

## 📖 References

- [PMC Study on Light and Mood](https://pmc.ncbi.nlm.nih.gov/articles/PMC7445808/) *(link provided, content unavailable)*
- [How Light Affects Mental Health – The Conversation](https://theconversation.com/how-light-can-shift-your-mood-and-mental-health-231282)
- [Lighting and Mood – Illuminated Integration](https://illuminated-integration.com/blog/how-lighting-affects-mood/)


---

Would you like help adding setup screenshots, demo videos, or a license section next?
