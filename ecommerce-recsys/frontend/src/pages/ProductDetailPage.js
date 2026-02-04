import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { StarIcon, HeartIcon, ShoppingCartIcon, TruckIcon, ShieldCheckIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarSolidIcon, HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';
import { useQuery } from 'react-query';
import { fetchProduct, fetchProductRecommendations } from '../utils/api';
import ProductCard from '../components/ProductCard';
import useStore from '../store/useStore';
import toast from 'react-hot-toast';

const ProductDetailPage = () => {
  const { id } = useParams();
  const [selectedSize, setSelectedSize] = useState('');
  const [selectedColor, setSelectedColor] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState(0);
  const [isWishlisted, setIsWishlisted] = useState(false);

  const { addToCart, isAuthenticated } = useStore();

  const { data: product, isLoading, error } = useQuery(
    ['product', id],
    () => fetchProduct(id),
    { staleTime: 5 * 60 * 1000 }
  );

  const { data: recommendations } = useQuery(
    ['product-recommendations', id],
    () => fetchProductRecommendations(id, 4),
    { 
      enabled: !!product,
      staleTime: 5 * 60 * 1000 
    }
  );

  const handleAddToCart = () => {
    if (!isAuthenticated) {
      toast.error('Please sign in to add items to cart');
      return;
    }

    if (product.sizes?.length > 0 && !selectedSize) {
      toast.error('Please select a size');
      return;
    }

    if (product.colors?.length > 0 && !selectedColor) {
      toast.error('Please select a color');
      return;
    }

    addToCart(product, quantity, selectedSize || 'One Size', selectedColor || 'Default');
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
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<StarSolidIcon key={i} className="h-5 w-5 text-yellow-400" />);
    }

    if (hasHalfStar) {
      stars.push(
        <div key="half" className="relative">
          <StarIcon className="h-5 w-5 text-gray-300" />
          <div className="absolute inset-0 overflow-hidden w-1/2">
            <StarSolidIcon className="h-5 w-5 text-yellow-400" />
          </div>
        </div>
      );
    }

    const remainingStars = 5 - Math.ceil(rating);
    for (let i = 0; i < remainingStars; i++) {
      stars.push(<StarIcon key={`empty-${i}`} className="h-5 w-5 text-gray-300" />);
    }

    return stars;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-gray-200 aspect-square rounded-lg"></div>
              <div className="space-y-4">
                <div className="h-8 bg-gray-200 rounded"></div>
                <div className="h-6 bg-gray-200 rounded w-2/3"></div>
                <div className="h-12 bg-gray-200 rounded"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Product not found</h2>
          <p className="text-gray-600">The product you're looking for doesn't exist.</p>
        </div>
      </div>
    );
  }

  const images = product.image_url ? [product.image_url] : ['https://via.placeholder.com/600x600?text=No+Image'];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Product Details */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden mb-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 p-8">
            {/* Product Images */}
            <div className="space-y-4">
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="aspect-square bg-gray-100 rounded-lg overflow-hidden"
              >
                <img
                  src={images[selectedImage]}
                  alt={product.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.target.src = 'https://via.placeholder.com/600x600?text=No+Image';
                  }}
                />
              </motion.div>
              
              {images.length > 1 && (
                <div className="flex space-x-2">
                  {images.map((image, index) => (
                    <button
                      key={index}
                      onClick={() => setSelectedImage(index)}
                      className={`w-20 h-20 rounded-lg overflow-hidden border-2 ${
                        selectedImage === index ? 'border-primary-600' : 'border-gray-200'
                      }`}
                    >
                      <img
                        src={image}
                        alt={`${product.name} ${index + 1}`}
                        className="w-full h-full object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Product Info */}
            <div className="space-y-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>
                {product.brand && (
                  <p className="text-lg text-gray-600 mb-4">by {product.brand}</p>
                )}
                
                {/* Rating */}
                <div className="flex items-center mb-4">
                  <div className="flex items-center">
                    {renderStars(product.rating)}
                  </div>
                  <span className="ml-2 text-sm text-gray-600">
                    {product.rating} ({product.review_count} reviews)
                  </span>
                </div>

                {/* Price */}
                <div className="flex items-center space-x-4 mb-6">
                  <span className="text-3xl font-bold text-gray-900">
                    {formatPrice(product.price)}
                  </span>
                  {product.original_price && product.price < product.original_price && (
                    <>
                      <span className="text-xl text-gray-500 line-through">
                        {formatPrice(product.original_price)}
                      </span>
                      <span className="bg-red-100 text-red-800 px-2 py-1 rounded-md text-sm font-medium">
                        {Math.round(((product.original_price - product.price) / product.original_price) * 100)}% OFF
                      </span>
                    </>
                  )}
                </div>
              </div>

              {/* Options */}
              <div className="space-y-4">
                {/* Size Selection */}
                {product.sizes && product.sizes.length > 0 && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Size
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {product.sizes.map((size) => (
                        <button
                          key={size}
                          onClick={() => setSelectedSize(size)}
                          className={`px-4 py-2 border rounded-lg font-medium ${
                            selectedSize === size
                              ? 'border-primary-600 bg-primary-50 text-primary-600'
                              : 'border-gray-300 text-gray-700 hover:border-gray-400'
                          }`}
                        >
                          {size}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Color Selection */}
                {product.colors && product.colors.length > 0 && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Color
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {product.colors.map((color) => (
                        <button
                          key={color}
                          onClick={() => setSelectedColor(color)}
                          className={`px-4 py-2 border rounded-lg font-medium ${
                            selectedColor === color
                              ? 'border-primary-600 bg-primary-50 text-primary-600'
                              : 'border-gray-300 text-gray-700 hover:border-gray-400'
                          }`}
                        >
                          {color}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Quantity */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Quantity
                  </label>
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => setQuantity(Math.max(1, quantity - 1))}
                      className="w-10 h-10 border border-gray-300 rounded-lg flex items-center justify-center hover:bg-gray-50"
                    >
                      -
                    </button>
                    <span className="text-lg font-medium w-12 text-center">{quantity}</span>
                    <button
                      onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                      className="w-10 h-10 border border-gray-300 rounded-lg flex items-center justify-center hover:bg-gray-50"
                    >
                      +
                    </button>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex space-x-4">
                <button
                  onClick={handleAddToCart}
                  disabled={product.stock === 0}
                  className="flex-1 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 text-white font-semibold py-3 px-6 rounded-lg flex items-center justify-center space-x-2 transition-colors"
                >
                  <ShoppingCartIcon className="h-5 w-5" />
                  <span>{product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}</span>
                </button>
                
                <button
                  onClick={() => setIsWishlisted(!isWishlisted)}
                  className="p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  {isWishlisted ? (
                    <HeartSolidIcon className="h-6 w-6 text-red-500" />
                  ) : (
                    <HeartIcon className="h-6 w-6 text-gray-600" />
                  )}
                </button>
              </div>

              {/* Features */}
              <div className="border-t pt-6 space-y-3">
                <div className="flex items-center space-x-3 text-sm text-gray-600">
                  <TruckIcon className="h-5 w-5" />
                  <span>Free shipping on orders over $50</span>
                </div>
                <div className="flex items-center space-x-3 text-sm text-gray-600">
                  <ShieldCheckIcon className="h-5 w-5" />
                  <span>30-day return policy</span>
                </div>
              </div>
            </div>
          </div>

          {/* Description */}
          {product.description && (
            <div className="border-t px-8 py-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Description</h3>
              <p className="text-gray-600 leading-relaxed">{product.description}</p>
            </div>
          )}
        </div>

        {/* Recommendations */}
        {recommendations && recommendations.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">You May Also Like</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {recommendations.map((product, index) => (
                <motion.div
                  key={product.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                >
                  <ProductCard product={product} />
                </motion.div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductDetailPage;