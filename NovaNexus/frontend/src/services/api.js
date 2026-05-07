import axios from 'axios';

// Use environment variable for production API, default to Render URL
const API_URL = import.meta.env.VITE_API_URL || 'https://forgemind-ai.onrender.com';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
