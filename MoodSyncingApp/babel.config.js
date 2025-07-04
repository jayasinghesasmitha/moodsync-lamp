module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      // Only include if you're using Reanimated
      'react-native-reanimated/plugin',
    ],
  };
};