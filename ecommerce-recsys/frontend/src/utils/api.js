import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Products API
export const fetchProducts = async (params = {}) => {
  const response = await api.get('/api/products', { params });
  return response.data;
};

export const fetchProduct = async (id) => {
  const response = await api.get(`/api/products/${id}`);
  return response.data;
};

export const fetchTrendingProducts = async () => {
  const response = await api.get('/api/products/trending');
  return response.data;
};

export const fetchRecommendations = async (userId) => {
  const response = await api.get(`/api/recommendations/user/${userId}`);
  return response.data;
};

export const fetchProductRecommendations = async (productId) => {
  const response = await api.get(`/api/recommendations/product/${productId}`);
  return response.data;
};

export default api;