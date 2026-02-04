import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { TrashIcon, PlusIcon, MinusIcon, ShoppingBagIcon } from '@heroicons/react/24/outline';
import useStore from '../store/useStore';
import toast from 'react-hot-toast';

const CartPage = () => {
  const { cart, cartCount, updateCartQuantity, removeFromCart, clearCart } = useStore();

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const calculateSubtotal = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const calculateTax = (subtotal) => {
    return subtotal * 0.08; // 8% tax
  };

  const calculateShipping = (subtotal) => {
    return subtotal > 50 ? 0 : 9.99;
  };

  const calculateTotal = () => {
    const subtotal = calculateSubtotal();
    const tax = calculateTax(subtotal);
    const shipping = calculateShipping(subtotal);
    return subtotal + tax + shipping;
  };

  const handleQuantityChange = (item, newQuantity) => {
    if (newQuantity < 1) {
      removeFromCart(item.id, item.size, item.color);
      toast.success('Item removed from cart');
    } else {
      updateCartQuantity(item.id, item.size, item.color, newQuantity);
    }
  };

  const handleRemoveItem = (item) => {
    removeFromCart(item.id, item.size, item.color);
    toast.success('Item removed from cart');
  };

  const handleClearCart = () => {
    clearCart();
    toast.success('Cart cleared');
  };

  if (cartCount === 0) {
    return (
      <div className="min-h-screen bg-gray-50 py-16">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <ShoppingBagIcon className="h-24 w-24 text-gray-300 mx-auto mb-6" />
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Your cart is empty</h2>
            <p className="text-gray-600 mb-8">
              Looks like you haven't added any items to your cart yet.
            </p>
            <Link
              to="/products"
              className="inline-flex items-center px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-colors"
            >
              Start Shopping
            </Link>
          </motion.div>
        </div>
      </div>
    );
  }

  const subtotal = calculateSubtotal();
  const tax = calculateTax(subtotal);
  const shipping = calculateShipping(subtotal);
  const total = calculateTotal();

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Shopping Cart</h1>
          <button
            onClick={handleClearCart}
            className="text-sm text-red-600 hover:text-red-700 font-medium"
          >
            Clear Cart
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2 space-y-4">
            {cart.map((item, index) => (
              <motion.div
                key={`${item.id}-${item.size}-${item.color}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
              >
                <div className="flex items-center space-x-4">
                  {/* Product Image */}
                  <div className="w-24 h-24 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
                    <img
                      src={item.image_url || 'https://via.placeholder.com/96x96?text=No+Image'}
                      alt={item.name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        e.target.src = 'https://via.placeholder.com/96x96?text=No+Image';
                      }}
                    />
                  </div>

                  {/* Product Details */}
                  <div className="flex-1 min-w-0">
                    <Link
                      to={`/product/${item.id}`}
                      className="text-lg font-semibold text-gray-900 hover:text-primary-600 transition-colors"
                    >
                      {item.name}
                    </Link>
                    {item.brand && (
                      <p className="text-sm text-gray-600 mt-1">{item.brand}</p>
                    )}
                    <div className="flex items-center space-x-4 mt-2 text-sm text-gray-600">
                      {item.size && item.size !== 'One Size' && (
                        <span>Size: {item.size}</span>
                      )}
                      {item.color && item.color !== 'Default' && (
                        <span>Color: {item.color}</span>
                      )}
                    </div>
                  </div>

                  {/* Quantity Controls */}
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => handleQuantityChange(item, item.quantity - 1)}
                      className="w-8 h-8 border border-gray-300 rounded-lg flex items-center justify-center hover:bg-gray-50 transition-colors"
                    >
                      <MinusIcon className="h-4 w-4" />
                    </button>
                    <span className="text-lg font-medium w-8 text-center">{item.quantity}</span>
                    <button
                      onClick={() => handleQuantityChange(item, item.quantity + 1)}
                      className="w-8 h-8 border border-gray-300 rounded-lg flex items-center justify-center hover:bg-gray-50 transition-colors"
                    >
                      <PlusIcon className="h-4 w-4" />
                    </button>
                  </div>

                  {/* Price */}
                  <div className="text-right">
                    <p className="text-lg font-semibold text-gray-900">
                      {formatPrice(item.price * item.quantity)}
                    </p>
                    <p className="text-sm text-gray-600">
                      {formatPrice(item.price)} each
                    </p>
                  </div>

                  {/* Remove Button */}
                  <button
                    onClick={() => handleRemoveItem(item)}
                    className="p-2 text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 sticky top-8"
            >
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Order Summary</h2>
              
              <div className="space-y-4">
                <div className="flex justify-between">
                  <span className="text-gray-600">Subtotal ({cartCount} items)</span>
                  <span className="font-medium">{formatPrice(subtotal)}</span>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-gray-600">Shipping</span>
                  <span className="font-medium">
                    {shipping === 0 ? 'Free' : formatPrice(shipping)}
                  </span>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-gray-600">Tax</span>
                  <span className="font-medium">{formatPrice(tax)}</span>
                </div>
                
                {shipping > 0 && (
                  <div className="text-sm text-gray-600 bg-blue-50 p-3 rounded-lg">
                    Add {formatPrice(50 - subtotal)} more for free shipping!
                  </div>
                )}
                
                <div className="border-t pt-4">
                  <div className="flex justify-between text-lg font-semibold">
                    <span>Total</span>
                    <span>{formatPrice(total)}</span>
                  </div>
                </div>
              </div>

              <button className="w-full mt-6 bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors">
                Proceed to Checkout
              </button>

              <Link
                to="/products"
                className="block w-full mt-3 text-center text-primary-600 hover:text-primary-700 font-medium py-2"
              >
                Continue Shopping
              </Link>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CartPage;