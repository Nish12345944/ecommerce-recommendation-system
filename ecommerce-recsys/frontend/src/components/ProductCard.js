import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { StarIcon, ShoppingCartIcon } from '@heroicons/react/24/solid';
import { HeartIcon as HeartOutlineIcon } from '@heroicons/react/24/outline';
import useStore from '../store/useStore';
import toast from 'react-hot-toast';

const ProductCard = ({ product }) => {
  const { addToCart } = useStore();

  const handleAddToCart = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    addToCart(product, 1, 'M', 'Default');
    toast.success('Added to cart!');
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);

    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <StarIcon key={i} className="h-4 w-4 text-yellow-400" />
      );
    }

    const remainingStars = 5 - fullStars;
    for (let i = 0; i < remainingStars; i++) {
      stars.push(
        <StarIcon key={`empty-${i}`} className="h-4 w-4 text-gray-300" />
      );
    }

    return stars;
  };

  return (
    <motion.div
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
      className="group"
    >
      <Link to={`/product/${product.id}`} className="block">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow duration-300">
          {/* Product Image */}
          <div className="relative aspect-square overflow-hidden bg-gray-100">
            <img
              src={product.image_url || 'https://via.placeholder.com/300x300?text=No+Image'}
              alt={product.name}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              onError={(e) => {
                e.target.src = 'https://via.placeholder.com/300x300?text=No+Image';
              }}
            />
            
            {/* Wishlist Button */}
            <button className="absolute top-3 right-3 p-2 bg-white rounded-full shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-gray-50">
              <HeartOutlineIcon className="h-5 w-5 text-gray-600" />
            </button>

            {/* Quick Add to Cart */}
            <button
              onClick={handleAddToCart}
              className="absolute bottom-3 right-3 p-2 bg-primary-600 text-white rounded-full shadow-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-primary-700"
            >
              <ShoppingCartIcon className="h-5 w-5" />
            </button>

            {/* Sale Badge */}
            {product.original_price && product.price < product.original_price && (
              <div className="absolute top-3 left-3 bg-red-500 text-white px-2 py-1 rounded-md text-xs font-medium">
                {Math.round(((product.original_price - product.price) / product.original_price) * 100)}% OFF
              </div>
            )}
          </div>

          {/* Product Info */}
          <div className="p-4">
            <div className="mb-2">
              <h3 className="text-sm font-medium text-gray-900 line-clamp-2 group-hover:text-primary-600 transition-colors">
                {product.name}
              </h3>
              {product.brand && (
                <p className="text-xs text-gray-500 mt-1">{product.brand}</p>
              )}
            </div>

            {/* Rating */}
            <div className="flex items-center mb-2">
              <div className="flex items-center">
                {renderStars(product.rating || 4.5)}
              </div>
              <span className="ml-2 text-xs text-gray-500">
                ({product.review_count || 0})
              </span>
            </div>

            {/* Price */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className="text-lg font-bold text-gray-900">
                  {formatPrice(product.price)}
                </span>
                {product.original_price && product.price < product.original_price && (
                  <span className="text-sm text-gray-500 line-through">
                    {formatPrice(product.original_price)}
                  </span>
                )}
              </div>
              
              {/* Stock Status */}
              {product.stock !== undefined && (
                <span className={`text-xs px-2 py-1 rounded-full ${
                  product.stock > 10 
                    ? 'bg-green-100 text-green-800' 
                    : product.stock > 0 
                    ? 'bg-yellow-100 text-yellow-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {product.stock > 10 ? 'In Stock' : product.stock > 0 ? `${product.stock} left` : 'Out of Stock'}
                </span>
              )}
            </div>
          </div>
        </div>
      </Link>
    </motion.div>
  );
};

export default ProductCard;