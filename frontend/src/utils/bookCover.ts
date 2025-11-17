/**
 * Get book cover URL from Open Library API
 * @param isbn - Book ISBN (10 or 13 digits)
 * @param size - Cover size: 'S' (small), 'M' (medium), 'L' (large)
 * @returns URL string for the book cover
 */
export function getBookCoverUrl(isbn: string, size: 'S' | 'M' | 'L' = 'M'): string {
  // Clean ISBN (remove hyphens and spaces)
  const cleanIsbn = isbn.replace(/[-\s]/g, '');
  
  // Open Library cover API
  // Format: https://covers.openlibrary.org/b/isbn/{ISBN}-{size}.jpg
  return `https://covers.openlibrary.org/b/isbn/${cleanIsbn}-${size}.jpg`;
}

/**
 * Get placeholder SVG for when book cover is not available
 */
export function getPlaceholderCover(): string {
  return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='600'%3E%3Crect fill='%23f3f4f6' width='400' height='600'/%3E%3Ctext x='50%25' y='50%25' font-size='80' text-anchor='middle' dominant-baseline='middle' fill='%239ca3af'%3E📚%3C/text%3E%3C/svg%3E";
}

