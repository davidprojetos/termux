npx react-native init appcommit
npm install @react-native/metro-config
nano metro.config.js

const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');

const config = {
  transformer: {},
  resolver: {
    sourceExts: ['js', 'jsx', 'ts', 'tsx', 'json'],
  },
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);

npx react-native start
