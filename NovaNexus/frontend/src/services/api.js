import axios from 'axios';

// Smart API URL detection
// 1. Use environment variable if set (for explicit configuration)
// 2. Use window.location.origin for relative deployment (Render, local, etc.)
const API_URL = import.meta.env.VITE_API_URL || window.location.origin;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15000,
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error("API Error:", error.response.status, error.response.data);
    } else if (error.request) {
      console.error("Network Error - No response from server:", error.request);
    } else {
      console.error("Error:", error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
