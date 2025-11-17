import { useState } from 'react';
import { Link } from 'react-router-dom';
import type { BookList } from '../types';
import { getBookCoverUrl } from '../utils/bookCover';

interface BookCardProps {
  book: BookList;
}

const conditionColors: Record<string, string> = {
  new: 'bg-green-100 text-green-800',
  like_new: 'bg-blue-100 text-blue-800',
  good: 'bg-yellow-100 text-yellow-800',
  fair: 'bg-orange-100 text-orange-800',
  poor: 'bg-red-100 text-red-800',
};

export default function BookCard({ book }: BookCardProps) {
  const [imageError, setImageError] = useState(false);
  const coverUrl = getBookCoverUrl(book.isbn, 'M');

  return (
    <Link to={`/books/${book.id}`} className="card block">
      <div className="h-64 bg-gray-100 overflow-hidden relative">
        {!imageError ? (
          <img
            src={coverUrl}
            alt={`${book.title} cover`}
            className="w-full h-full object-contain bg-white"
            onError={() => setImageError(true)}
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center">
            <div className="text-center">
              <div className="text-6xl mb-2">📚</div>
              <div className="text-primary-700 font-semibold text-sm">No Cover</div>
            </div>
          </div>
        )}
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-lg mb-2 line-clamp-2">{book.title}</h3>
        <p className="text-sm text-gray-600 mb-2">by {book.author_name}</p>
        <div className="flex items-center justify-between mb-2">
          <span className={`text-xs px-2 py-1 rounded ${conditionColors[book.condition] || conditionColors.good}`}>
            {book.condition.replace('_', ' ')}
          </span>
          <span className="text-sm text-gray-500">Qty: {book.quantity}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-2xl font-bold text-primary-600">${parseFloat(book.price).toFixed(2)}</span>
          {book.is_available ? (
            <span className="text-xs text-green-600 font-medium">In Stock</span>
          ) : (
            <span className="text-xs text-red-600 font-medium">Out of Stock</span>
          )}
        </div>
      </div>
    </Link>
  );
}

