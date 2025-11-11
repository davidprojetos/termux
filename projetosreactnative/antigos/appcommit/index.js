import { AppRegistry } from 'react-native';
import App from './App';
import { name as appName } from './app.json';
import { createRoot } from 'react-dom/client';
import { AppContainer } from 'react-hot-loader';

const root = createRoot(document.getElementById('root'));
root.render(
  <AppContainer>
    <App />
  </AppContainer>
);

AppRegistry.registerComponent(appName, () => App);