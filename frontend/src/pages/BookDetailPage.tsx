import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { bookService } from '../services/bookService';
import { useCartStore } from '../stores/cartStore';
import { useAuthStore } from '../stores/authStore';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { getBookCoverUrl } from '../utils/bookCover';

const conditionLabels: Record<string, string> = {
  new: 'New',
  like_new: 'Like New',
  good: 'Good',
  fair: 'Fair',
  poor: 'Poor',
};

export default function BookDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();
  const { addToCart, isLoading: cartLoading } = useCartStore();
  const [quantity, setQuantity] = useState(1);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [imageError, setImageError] = useState(false);

  const { data: book, isLoading } = useQuery({
    queryKey: ['book', id],
    queryFn: () => bookService.getBook(Number(id)),
    enabled: !!id,
  });

  const handleAddToCart = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    setError(null);
    setSuccess(false);

    try {
      await addToCart(book!.id, quantity);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err: any) {
      setError(err.error || 'Failed to add to cart');
    }
  };

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!book) {
    return (
      <div className="container mx-auto px-4 py-8">
        <ErrorMessage message="Book not found" />
      </div>
    );
  }

  const maxQuantity = Math.min(book.quantity, 10);
  const coverUrl = getBookCoverUrl(book.isbn, 'L');

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <div className="h-96 bg-gray-100 rounded-lg overflow-hidden mb-4 relative">
            {!imageError ? (
              <img
                src={coverUrl}
                alt={`${book.title} cover`}
                className="w-full h-full object-contain bg-white"
                onError={() => setImageError(true)}
              />
            ) : (
              <div className="w-full h-full bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center">
                <div className="text-center">
                  <div className="text-9xl mb-4">📚</div>
                  <div className="text-primary-700 font-semibold">No Cover Available</div>
                </div>
              </div>
            )}
          </div>
        </div>

        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">{book.title}</h1>
          <p className="text-xl text-gray-600 mb-4">by {book.author.name}</p>

          <div className="mb-6">
            <span className="text-3xl font-bold text-primary-600">${parseFloat(book.price).toFixed(2)}</span>
            <span className="ml-4 text-sm text-gray-500">
              {book.is_available ? `In Stock (${book.quantity} available)` : 'Out of Stock'}
            </span>
          </div>

          <div className="space-y-4 mb-6">
            <div>
              <span className="font-semibold">Condition:</span>{' '}
              <span className="px-2 py-1 bg-gray-100 rounded">{conditionLabels[book.condition]}</span>
            </div>
            <div>
              <span className="font-semibold">ISBN:</span> {book.isbn}
            </div>
            {book.pages && (
              <div>
                <span className="font-semibold">Pages:</span> {book.pages}
              </div>
            )}
            <div>
              <span className="font-semibold">Publisher:</span> {book.editorial.name}
            </div>
            {book.publication_date && (
              <div>
                <span className="font-semibold">Published:</span>{' '}
                {new Date(book.publication_date).getFullYear()}
              </div>
            )}
          </div>

          {book.description && (
            <div className="mb-6">
              <h3 className="font-semibold mb-2">Description</h3>
              <p className="text-gray-700">{book.description}</p>
            </div>
          )}

          {book.is_available && (
            <div className="border-t pt-6">
              {error && <ErrorMessage message={error} onClose={() => setError(null)} />}
              {success && (
                <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-4">
                  Item added to cart successfully!
                </div>
              )}

              <div className="flex items-center gap-4 mb-4">
                <label className="font-semibold">Quantity:</label>
                <input
                  type="number"
                  min="1"
                  max={maxQuantity}
                  value={quantity}
                  onChange={(e) => setQuantity(Math.max(1, Math.min(maxQuantity, parseInt(e.target.value) || 1)))}
                  className="input w-20"
                />
                <span className="text-sm text-gray-500">(max {maxQuantity})</span>
              </div>

              <button
                onClick={handleAddToCart}
                disabled={cartLoading || !book.is_available}
                className="btn-primary w-full text-lg py-3"
              >
                {cartLoading ? 'Adding...' : 'Add to Cart'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

