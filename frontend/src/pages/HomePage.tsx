import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { bookService } from '../services/bookService';
import BookList from '../components/BookList';
import SearchBar from '../components/SearchBar';

export default function HomePage() {
  const [searchQuery, setSearchQuery] = useState('');

  const { data, isLoading } = useQuery({
    queryKey: ['books', searchQuery],
    queryFn: () => bookService.getAllBooks({ search: searchQuery }),
  });

  const books = data?.results || [];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Welcome to Our Bookstore</h1>
        <p className="text-lg text-gray-600 mb-6">
          Discover your next favorite book from our collection of classic literature
        </p>
        <SearchBar onSearch={setSearchQuery} />
      </div>

      <div className="mb-6">
        <h2 className="text-2xl font-semibold mb-4">Featured Books</h2>
        <BookList books={books.slice(0, 8)} isLoading={isLoading} />
      </div>

      {books.length > 8 && (
        <div className="text-center mt-8">
          <a href="/books" className="btn-primary">
            View All Books
          </a>
        </div>
      )}
    </div>
  );
}

