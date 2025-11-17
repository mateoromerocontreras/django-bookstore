import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useCartStore } from '../stores/cartStore';
import type { CartItem as CartItemType } from '../types';
import { getBookCoverUrl } from '../utils/bookCover';

interface CartItemProps {
  item: CartItemType;
}

export default function CartItem({ item }: CartItemProps) {
  const { updateCartItem, removeFromCart, isLoading } = useCartStore();
  const maxQuantity = Math.min(item.book.quantity, 10);
  const [imageError, setImageError] = useState(false);
  const coverUrl = getBookCoverUrl(item.book.isbn, 'S');

  const handleQuantityChange = async (newQuantity: number) => {
    if (newQuantity < 1) return;
    if (newQuantity > maxQuantity) return;
    try {
      await updateCartItem(item.book.id, newQuantity);
    } catch (error) {
      console.error('Failed to update quantity:', error);
    }
  };

  const handleRemove = async () => {
    try {
      await removeFromCart(item.book.id);
    } catch (error) {
      console.error('Failed to remove item:', error);
    }
  };

  return (
    <div className="flex items-center gap-4 p-4 border-b border-gray-200">
      <Link to={`/books/${item.book.id}`} className="flex-shrink-0">
        <div className="w-20 h-20 bg-gray-100 rounded overflow-hidden">
          {!imageError ? (
            <img
              src={coverUrl}
              alt={`${item.book.title} cover`}
              className="w-full h-full object-contain bg-white"
              onError={() => setImageError(true)}
            />
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center">
              <span className="text-2xl">📚</span>
            </div>
          )}
        </div>
      </Link>

      <div className="flex-grow">
        <Link to={`/books/${item.book.id}`} className="hover:text-primary-600">
          <h3 className="font-semibold text-lg">{item.book.title}</h3>
          <p className="text-sm text-gray-600">by {item.book.author.name}</p>
        </Link>
        <p className="text-primary-600 font-semibold mt-1">${parseFloat(item.book.price).toFixed(2)}</p>
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={() => handleQuantityChange(item.quantity - 1)}
          disabled={isLoading || item.quantity <= 1}
          className="w-8 h-8 rounded border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
        >
          −
        </button>
        <span className="w-12 text-center font-medium">{item.quantity}</span>
        <button
          onClick={() => handleQuantityChange(item.quantity + 1)}
          disabled={isLoading || item.quantity >= maxQuantity}
          className="w-8 h-8 rounded border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
        >
          +
        </button>
      </div>

      <div className="text-right min-w-[100px]">
        <p className="font-semibold text-lg">${parseFloat(item.subtotal).toFixed(2)}</p>
        <button
          onClick={handleRemove}
          disabled={isLoading}
          className="text-sm text-red-600 hover:text-red-700 mt-1 disabled:opacity-50"
        >
          Remove
        </button>
      </div>
    </div>
  );
}

