import axios from 'axios';

// Use environment variable for production API, default to localhost for development
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:10000/api';

const api = axios.create({
  baseURL: API_URL,
});

export default api;
