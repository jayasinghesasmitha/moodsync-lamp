import { AppRegistry } from 'react-native';
import App from './App'; // Ensure App component is defined correctly
import { name as appName } from './app.json';

AppRegistry.registerComponent(appName, () => App);
