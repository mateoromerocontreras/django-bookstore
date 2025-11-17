import BookCard from './BookCard';
import LoadingSpinner from './LoadingSpinner';
import type { BookList as BookListType } from '../types';

interface BookListProps {
  books: BookListType[];
  isLoading?: boolean;
}

export default function BookList({ books, isLoading }: BookListProps) {
  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (books.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No books found.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {books.map((book) => (
        <BookCard key={book.id} book={book} />
      ))}
    </div>
  );
}

