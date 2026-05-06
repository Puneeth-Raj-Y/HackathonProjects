import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const OrderService = {
  getOrders: (status) => api.get('/orders/', { params: { status } }),
  getOrderStats: () => api.get('/orders/stats/summary'),
  sendMessage: (message) => api.post('/chat/', { message }),
};

export default api;
