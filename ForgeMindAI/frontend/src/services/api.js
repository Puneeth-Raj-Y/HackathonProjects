import axios from 'axios';

const api = axios.create({
  baseURL: window.location.origin,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;
    const payload = error.response?.data;
    console.error('ForgeMind API error:', status, payload || error.message);
    return Promise.reject(error);
  }
);

export default api;
