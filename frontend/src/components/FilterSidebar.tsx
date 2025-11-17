import { useEffect } from 'react';
import { useBookStore } from '../stores/bookStore';
import { authorService } from '../services/authorService';

export default function FilterSidebar() {
  const { filters, authors, setFilter, resetFilters, setAuthors } = useBookStore();

  useEffect(() => {
    const loadAuthors = async () => {
      try {
        const data = await authorService.getAllAuthors();
        // Ensure data is an array
        if (Array.isArray(data)) {
          setAuthors(data);
        } else {
          console.error('Authors data is not an array:', data);
          setAuthors([]);
        }
      } catch (error) {
        console.error('Failed to load authors:', error);
        setAuthors([]);
      }
    };
    loadAuthors();
  }, [setAuthors]);

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">Filters</h3>
        <button
          onClick={resetFilters}
          className="text-sm text-primary-600 hover:text-primary-700"
        >
          Reset
        </button>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Author
          </label>
          <select
            value={filters.author || ''}
            onChange={(e) => setFilter('author', e.target.value ? parseInt(e.target.value) : null)}
            className="input"
          >
            <option value="">All Authors</option>
            {Array.isArray(authors) && authors.map((author) => (
              <option key={author.id} value={author.id}>
                {author.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Condition
          </label>
          <select
            value={filters.condition || ''}
            onChange={(e) => setFilter('condition', e.target.value || null)}
            className="input"
          >
            <option value="">All Conditions</option>
            <option value="new">New</option>
            <option value="like_new">Like New</option>
            <option value="good">Good</option>
            <option value="fair">Fair</option>
            <option value="poor">Poor</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Price Range
          </label>
          <div className="grid grid-cols-2 gap-2">
            <input
              type="number"
              placeholder="Min"
              value={filters.minPrice || ''}
              onChange={(e) => setFilter('minPrice', e.target.value ? parseFloat(e.target.value) : null)}
              className="input"
            />
            <input
              type="number"
              placeholder="Max"
              value={filters.maxPrice || ''}
              onChange={(e) => setFilter('maxPrice', e.target.value ? parseFloat(e.target.value) : null)}
              className="input"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

