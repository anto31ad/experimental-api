
const API_HOST = import.meta.env.VITE_API_HOST;
const API_PORT = import.meta.env.VITE_API_PORT;

const API_ADDRESS = `http://${API_HOST}:${API_PORT}`;

const STUB_MODE = import.meta.env.VITE_STUB_MODE === 'true';

export const AUTH_TOKEN_KEY = 'experimentalApi_token';

export const API_ENDPOINTS = {
  root: API_ADDRESS,
  login: `${API_ADDRESS}/token`,
  loginWithGitHub: `${API_ADDRESS}/login/github`,
  logout: `${API_ADDRESS}/logout`,
  thisUser: `${API_ADDRESS}/users/me`, 
  services: `${API_ADDRESS}/services`,
}

export const DEV_OPTIONS = {
  stubModeOn: STUB_MODE,
  stubServicesPath: '/stubModels.json',
}
