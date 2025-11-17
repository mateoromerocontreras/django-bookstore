import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { bookService } from '../services/bookService';
import BookList from '../components/BookList';
import SearchBar from '../components/SearchBar';
import FilterSidebar from '../components/FilterSidebar';
import { useBookStore } from '../stores/bookStore';

export default function BooksPage() {
  const { filters } = useBookStore();
  const [searchQuery, setSearchQuery] = useState('');

  const { data, isLoading } = useQuery({
    queryKey: ['books', filters, searchQuery],
    queryFn: () => bookService.getAllBooks({ search: searchQuery }),
  });

  const books = data?.results || [];

  // Apply filters client-side (in a real app, you'd do this server-side)
  const filteredBooks = books.filter((book) => {
    if (filters.author && book.author_name) {
      // This would need author_id in BookList type, but for now we'll skip author filter
    }
    if (filters.condition && book.condition !== filters.condition) {
      return false;
    }
    const price = parseFloat(book.price);
    if (filters.minPrice && price < filters.minPrice) {
      return false;
    }
    if (filters.maxPrice && price > filters.maxPrice) {
      return false;
    }
    return true;
  });

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">All Books</h1>
        <SearchBar onSearch={setSearchQuery} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-1">
          <FilterSidebar />
        </div>
        <div className="lg:col-span-3">
          <div className="mb-4">
            <p className="text-gray-600">
              Showing {filteredBooks.length} {filteredBooks.length === 1 ? 'book' : 'books'}
            </p>
          </div>
          <BookList books={filteredBooks} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
}

