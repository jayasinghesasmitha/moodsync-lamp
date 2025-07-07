1.Install Node.js, then install Expo CLI:

bash
npm install -g expo-cli
Create a new project:

bash
expo init MoodSyncingApp
cd MoodSyncingApp

2.Install dependencies with correct versions:
npm install --legacy-peer-deps

3.Install React Navigation packages separately:
npx expo install @react-navigation/native@6.1.9
npx expo install @react-navigation/stack@6.3.19
npx expo install react-native-screens@3.29.0
npx expo install react-native-safe-area-context@4.7.2
npx expo install expo-camera@13.5.0
npm install firebase@10.11.0

4.Fixing Package Version Warnings
npx expo install @expo/metro-config@~0.17.1
npx expo install @expo/metro-runtime@~3.1.3
npx expo install expo-camera@~14.1.3
npx expo install react-native@0.73.6
npx expo install react-native-safe-area-context@4.8.2

5.If it does not work
Run these commands in your project directory:

powershell
npx expo install @expo/metro-config@~0.17.1
npx expo install @expo/metro-runtime@~3.1.3
npx expo install expo-camera@~14.1.3
npx expo install react-native@0.73.6
npx expo install react-native-safe-area-context@4.8.2
npx expo install @react-navigation/native@^6.x
npx expo install @react-navigation/stack@^6.x
npx expo install react-native-gesture-handler@~2.12.0
npm install --save firebase@^10.11.0
npx expo install expo-linear-gradient

6.run the project
npx expo start

7.click w 

8.Other libraries
npx expo install expo-av
npx expo install expo-media-library

9.To connect with the firebase(if it is not working under guven environment)
npm uninstall firebase
npm install firebase@8