import React, { useEffect, useState } from 'react';
import * as mqtt from 'react-native-mqtt';

const BuildConnection = ({ moodData }) => {
  const [client, setClient] = useState(null);

  useEffect(() => {
    console.log('BuildConnection: Initializing MQTT client');
    const mqttClient = mqtt.connect('mqtt://broker.hivemq.com:1883', {
      clientId: 'MoodApp_' + Math.random().toString(16).slice(3),
    });

    mqttClient.on('connect', () => {
      console.log('BuildConnection: MQTT Connected');
      mqttClient.subscribe('MOODSYNC', 0, (err) => {
        console.log(err ? 'BuildConnection: MQTT Subscription error' : 'BuildConnection: Subscribed to MOODSYNC');
      });
    });

    mqttClient.on('error', (err) => {
      console.error('BuildConnection: MQTT Error:', err);
    });

    setClient(mqttClient);

    return () => {
      console.log('BuildConnection: Closing MQTT');
      if (mqttClient) mqttClient.end();
    };
  }, []);

  useEffect(() => {
    if (moodData && client) {
      const message = JSON.stringify(moodData);
      console.log('BuildConnection: Publishing to MOODSYNC:', message);
      client.publish('MOODSYNC', message, { qos: 0 }, (err) => {
        console.log(err ? 'BuildConnection: MQTT Publish error' : 'BuildConnection: MQTT Publish successful');
      });
    }
  }, [moodData, client]);

  return null; // No UI rendering
};

export default BuildConnection;