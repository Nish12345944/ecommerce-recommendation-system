import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useStore = create(
  persist(
    (set, get) => ({
      // Cart state
      cart: [],
      cartCount: 0,
      
      // Actions
      addToCart: (product, quantity = 1, size, color) => {
        const { cart } = get();
        const existingItem = cart.find(
          item => item.id === product.id && item.size === size && item.color === color
        );
        
        if (existingItem) {
          set({
            cart: cart.map(item =>
              item.id === product.id && item.size === size && item.color === color
                ? { ...item, quantity: item.quantity + quantity }
                : item
            ),
            cartCount: get().cartCount + quantity
          });
        } else {
          set({
            cart: [...cart, { ...product, quantity, size, color }],
            cartCount: get().cartCount + quantity
          });
        }
      },
      
      removeFromCart: (productId, size, color) => {
        const { cart } = get();
        const item = cart.find(item => item.id === productId && item.size === size && item.color === color);
        if (item) {
          set({
            cart: cart.filter(item => !(item.id === productId && item.size === size && item.color === color)),
            cartCount: get().cartCount - item.quantity
          });
        }
      },
      
      updateCartQuantity: (productId, size, color, quantity) => {
        const { cart } = get();
        const oldItem = cart.find(item => item.id === productId && item.size === size && item.color === color);
        if (oldItem) {
          const quantityDiff = quantity - oldItem.quantity;
          set({
            cart: cart.map(item =>
              item.id === productId && item.size === size && item.color === color
                ? { ...item, quantity }
                : item
            ),
            cartCount: get().cartCount + quantityDiff
          });
        }
      },
      
      clearCart: () => set({ cart: [], cartCount: 0 }),
    }),
    {
      name: 'ecommerce-store',
      partialize: (state) => ({
        cart: state.cart,
        cartCount: state.cartCount,
      }),
    }
  )
);

export default useStore;