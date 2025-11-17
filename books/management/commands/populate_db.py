from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Author, Editorial, Book
from decimal import Decimal
from datetime import date
import random


class Command(BaseCommand):
    help = 'Populates the database with classic books, authors, and editorials'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Create sample users (sellers)
        users = self.create_users()

        # Create authors
        authors = self.create_authors()

        # Create editorials
        editorials = self.create_editorials()

        # Create books
        self.create_books(authors, editorials, users)

        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))

    def create_users(self):
        """Create sample user accounts"""
        users = []
        user_data = [
            {'username': 'booklover1', 'email': 'booklover1@example.com', 'first_name': 'Alice', 'last_name': 'Johnson'},
            {'username': 'reader2', 'email': 'reader2@example.com', 'first_name': 'Bob', 'last_name': 'Smith'},
            {'username': 'bibliophile', 'email': 'bibliophile@example.com', 'first_name': 'Carol', 'last_name': 'Williams'},
            {'username': 'bookcollector', 'email': 'bookcollector@example.com', 'first_name': 'David', 'last_name': 'Brown'},
            {'username': 'literaturefan', 'email': 'literaturefan@example.com', 'first_name': 'Emma', 'last_name': 'Davis'},
        ]

        for user_info in user_data:
            user, created = User.objects.get_or_create(
                username=user_info['username'],
                defaults={
                    'email': user_info['email'],
                    'first_name': user_info['first_name'],
                    'last_name': user_info['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            users.append(user)

        return users

    def create_authors(self):
        """Create classic authors"""
        authors_data = [
            {
                'name': 'Jane Austen',
                'bio': 'English novelist known primarily for her six major novels, which interpret, critique and comment upon the British landed gentry at the end of the 18th century.',
                'birth_date': date(1775, 12, 16),
                'nationality': 'British'
            },
            {
                'name': 'Charles Dickens',
                'bio': 'English writer and social critic. He created some of the world\'s best-known fictional characters and is regarded as the greatest novelist of the Victorian era.',
                'birth_date': date(1812, 2, 7),
                'nationality': 'British'
            },
            {
                'name': 'Mark Twain',
                'bio': 'American writer, humorist, entrepreneur, publisher, and lecturer. He was lauded as the "greatest humorist the United States has produced".',
                'birth_date': date(1835, 11, 30),
                'nationality': 'American'
            },
            {
                'name': 'Leo Tolstoy',
                'bio': 'Russian writer who is regarded as one of the greatest authors of all time. He received nominations for the Nobel Prize in Literature every year from 1902 to 1906.',
                'birth_date': date(1828, 9, 9),
                'nationality': 'Russian'
            },
            {
                'name': 'Fyodor Dostoevsky',
                'bio': 'Russian novelist, short story writer, essayist, and journalist. His literary works explore human psychology in the troubled political, social, and spiritual atmospheres of 19th-century Russia.',
                'birth_date': date(1821, 11, 11),
                'nationality': 'Russian'
            },
            {
                'name': 'Virginia Woolf',
                'bio': 'English writer, considered one of the most important modernist 20th-century authors and a pioneer in the use of stream of consciousness as a narrative device.',
                'birth_date': date(1882, 1, 25),
                'nationality': 'British'
            },
            {
                'name': 'Ernest Hemingway',
                'bio': 'American novelist, short-story writer, and journalist. His economical and understated style had a strong influence on 20th-century fiction.',
                'birth_date': date(1899, 7, 21),
                'nationality': 'American'
            },
            {
                'name': 'George Orwell',
                'bio': 'English novelist, essayist, journalist and critic. His work is characterised by lucid prose, social criticism, opposition to totalitarianism, and support of democratic socialism.',
                'birth_date': date(1903, 6, 25),
                'nationality': 'British'
            },
            {
                'name': 'J.D. Salinger',
                'bio': 'American writer known for his widely read novel "The Catcher in the Rye". His reputation was built on a foundation of critical acclaim and public curiosity.',
                'birth_date': date(1919, 1, 1),
                'nationality': 'American'
            },
            {
                'name': 'Harper Lee',
                'bio': 'American novelist best known for her 1960 novel "To Kill a Mockingbird", which won the 1961 Pulitzer Prize and became a classic of modern American literature.',
                'birth_date': date(1926, 4, 28),
                'nationality': 'American'
            },
        ]

        authors = []
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                name=author_data['name'],
                defaults=author_data
            )
            if created:
                self.stdout.write(f'Created author: {author.name}')
            authors.append(author)

        return authors

    def create_editorials(self):
        """Create publishing houses"""
        editorials_data = [
            {
                'name': 'Penguin Classics',
                'address': '80 Strand, London WC2R 0RL, United Kingdom',
                'phone': '+44 20 7010 3000',
                'email': 'info@penguin.co.uk',
                'website': 'https://www.penguin.co.uk'
            },
            {
                'name': 'HarperCollins',
                'address': '195 Broadway, New York, NY 10007, USA',
                'phone': '+1 212 207 7000',
                'email': 'info@harpercollins.com',
                'website': 'https://www.harpercollins.com'
            },
            {
                'name': 'Random House',
                'address': '1745 Broadway, New York, NY 10019, USA',
                'phone': '+1 212 782 9000',
                'email': 'info@randomhouse.com',
                'website': 'https://www.randomhouse.com'
            },
            {
                'name': 'Simon & Schuster',
                'address': '1230 Avenue of the Americas, New York, NY 10020, USA',
                'phone': '+1 212 698 7000',
                'email': 'info@simonandschuster.com',
                'website': 'https://www.simonandschuster.com'
            },
            {
                'name': 'Vintage Books',
                'address': '1745 Broadway, New York, NY 10019, USA',
                'phone': '+1 212 782 9000',
                'email': 'info@vintagebooks.com',
                'website': 'https://www.vintagebooks.com'
            },
        ]

        editorials = []
        for editorial_data in editorials_data:
            editorial, created = Editorial.objects.get_or_create(
                name=editorial_data['name'],
                defaults=editorial_data
            )
            if created:
                self.stdout.write(f'Created editorial: {editorial.name}')
            editorials.append(editorial)

        return editorials

    def create_books(self, authors, editorials, users):
        """Create classic books"""
        books_data = [
            # Jane Austen books
            {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'isbn': '9780141439518', 'publication_date': date(1813, 1, 28), 'pages': 432, 'price': Decimal('12.99')},
            {'title': 'Sense and Sensibility', 'author': 'Jane Austen', 'isbn': '9780141439662', 'publication_date': date(1811, 10, 30), 'pages': 384, 'price': Decimal('11.50')},
            {'title': 'Emma', 'author': 'Jane Austen', 'isbn': '9780141439587', 'publication_date': date(1815, 12, 23), 'pages': 512, 'price': Decimal('13.25')},
            {'title': 'Mansfield Park', 'author': 'Jane Austen', 'isbn': '9780141439808', 'publication_date': date(1814, 7, 9), 'pages': 480, 'price': Decimal('12.75')},
            {'title': 'Persuasion', 'author': 'Jane Austen', 'isbn': '9780141439686', 'publication_date': date(1817, 12, 20), 'pages': 272, 'price': Decimal('10.99')},
            {'title': 'Northanger Abbey', 'author': 'Jane Austen', 'isbn': '9780141439792', 'publication_date': date(1817, 12, 20), 'pages': 256, 'price': Decimal('10.50')},

            # Charles Dickens books
            {'title': 'Great Expectations', 'author': 'Charles Dickens', 'isbn': '9780141439563', 'publication_date': date(1861, 8, 1), 'pages': 544, 'price': Decimal('14.50')},
            {'title': 'A Tale of Two Cities', 'author': 'Charles Dickens', 'isbn': '9780141439600', 'publication_date': date(1859, 4, 30), 'pages': 448, 'price': Decimal('13.99')},
            {'title': 'David Copperfield', 'author': 'Charles Dickens', 'isbn': '9780141439167', 'publication_date': date(1850, 11, 1), 'pages': 1024, 'price': Decimal('18.99')},
            {'title': 'Oliver Twist', 'author': 'Charles Dickens', 'isbn': '9780141439747', 'publication_date': date(1838, 2, 1), 'pages': 608, 'price': Decimal('15.25')},
            {'title': 'A Christmas Carol', 'author': 'Charles Dickens', 'isbn': '9780141389479', 'publication_date': date(1843, 12, 19), 'pages': 112, 'price': Decimal('8.99')},
            {'title': 'Bleak House', 'author': 'Charles Dickens', 'isbn': '9780141439723', 'publication_date': date(1853, 3, 1), 'pages': 1032, 'price': Decimal('19.50')},
            {'title': 'Hard Times', 'author': 'Charles Dickens', 'isbn': '9780141439679', 'publication_date': date(1854, 4, 1), 'pages': 368, 'price': Decimal('12.99')},

            # Mark Twain books
            {'title': 'The Adventures of Tom Sawyer', 'author': 'Mark Twain', 'isbn': '9780143039563', 'publication_date': date(1876, 6, 1), 'pages': 256, 'price': Decimal('11.99')},
            {'title': 'Adventures of Huckleberry Finn', 'author': 'Mark Twain', 'isbn': '9780143039563', 'publication_date': date(1884, 12, 10), 'pages': 366, 'price': Decimal('12.50')},
            {'title': 'The Prince and the Pauper', 'author': 'Mark Twain', 'isbn': '9780143039563', 'publication_date': date(1881, 12, 1), 'pages': 240, 'price': Decimal('10.75')},
            {'title': 'A Connecticut Yankee in King Arthur\'s Court', 'author': 'Mark Twain', 'isbn': '9780140430648', 'publication_date': date(1889, 12, 1), 'pages': 416, 'price': Decimal('13.25')},
            {'title': 'Life on the Mississippi', 'author': 'Mark Twain', 'isbn': '9780140390508', 'publication_date': date(1883, 5, 1), 'pages': 384, 'price': Decimal('12.99')},

            # Leo Tolstoy books
            {'title': 'War and Peace', 'author': 'Leo Tolstoy', 'isbn': '9780140447934', 'publication_date': date(1869, 1, 1), 'pages': 1392, 'price': Decimal('24.99')},
            {'title': 'Anna Karenina', 'author': 'Leo Tolstoy', 'isbn': '9780143035008', 'publication_date': date(1877, 1, 1), 'pages': 864, 'price': Decimal('19.99')},
            {'title': 'The Death of Ivan Ilyich', 'author': 'Leo Tolstoy', 'isbn': '9780140447927', 'publication_date': date(1886, 1, 1), 'pages': 128, 'price': Decimal('9.99')},
            {'title': 'Resurrection', 'author': 'Leo Tolstoy', 'isbn': '9780140448955', 'publication_date': date(1899, 1, 1), 'pages': 592, 'price': Decimal('16.50')},
            {'title': 'The Cossacks', 'author': 'Leo Tolstoy', 'isbn': '9780140449594', 'publication_date': date(1863, 1, 1), 'pages': 176, 'price': Decimal('10.99')},
            {'title': 'Childhood, Boyhood, Youth', 'author': 'Leo Tolstoy', 'isbn': '9780140449921', 'publication_date': date(1856, 1, 1), 'pages': 400, 'price': Decimal('14.25')},

            # Fyodor Dostoevsky books
            {'title': 'Crime and Punishment', 'author': 'Fyodor Dostoevsky', 'isbn': '9780140449136', 'publication_date': date(1866, 1, 1), 'pages': 671, 'price': Decimal('16.99')},
            {'title': 'The Brothers Karamazov', 'author': 'Fyodor Dostoevsky', 'isbn': '9780140449242', 'publication_date': date(1880, 1, 1), 'pages': 824, 'price': Decimal('20.50')},
            {'title': 'The Idiot', 'author': 'Fyodor Dostoevsky', 'isbn': '9780140445879', 'publication_date': date(1869, 1, 1), 'pages': 656, 'price': Decimal('17.75')},
            {'title': 'Notes from Underground', 'author': 'Fyodor Dostoevsky', 'isbn': '9780140442526', 'publication_date': date(1864, 1, 1), 'pages': 176, 'price': Decimal('10.50')},
            {'title': 'Demons', 'author': 'Fyodor Dostoevsky', 'isbn': '9780141441412', 'publication_date': date(1872, 1, 1), 'pages': 768, 'price': Decimal('19.25')},
            {'title': 'The Gambler', 'author': 'Fyodor Dostoevsky', 'isbn': '9780140441406', 'publication_date': date(1867, 1, 1), 'pages': 144, 'price': Decimal('9.75')},

            # Virginia Woolf books
            {'title': 'Mrs. Dalloway', 'author': 'Virginia Woolf', 'isbn': '9780156628709', 'publication_date': date(1925, 5, 14), 'pages': 194, 'price': Decimal('11.99')},
            {'title': 'To the Lighthouse', 'author': 'Virginia Woolf', 'isbn': '9780156907392', 'publication_date': date(1927, 5, 5), 'pages': 209, 'price': Decimal('12.50')},
            {'title': 'Orlando', 'author': 'Virginia Woolf', 'isbn': '9780156701600', 'publication_date': date(1928, 10, 11), 'pages': 333, 'price': Decimal('13.25')},
            {'title': 'The Waves', 'author': 'Virginia Woolf', 'isbn': '9780156949606', 'publication_date': date(1931, 10, 8), 'pages': 297, 'price': Decimal('12.99')},
            {'title': 'A Room of One\'s Own', 'author': 'Virginia Woolf', 'isbn': '9780156787338', 'publication_date': date(1929, 10, 24), 'pages': 112, 'price': Decimal('9.99')},
            {'title': 'The Years', 'author': 'Virginia Woolf', 'isbn': '9780156992084', 'publication_date': date(1937, 3, 15), 'pages': 469, 'price': Decimal('15.50')},

            # Ernest Hemingway books
            {'title': 'The Old Man and the Sea', 'author': 'Ernest Hemingway', 'isbn': '9780684801223', 'publication_date': date(1952, 9, 1), 'pages': 127, 'price': Decimal('10.99')},
            {'title': 'The Sun Also Rises', 'author': 'Ernest Hemingway', 'isbn': '9780743297332', 'publication_date': date(1926, 10, 22), 'pages': 251, 'price': Decimal('12.99')},
            {'title': 'A Farewell to Arms', 'author': 'Ernest Hemingway', 'isbn': '9780684801469', 'publication_date': date(1929, 9, 27), 'pages': 332, 'price': Decimal('13.50')},
            {'title': 'For Whom the Bell Tolls', 'author': 'Ernest Hemingway', 'isbn': '9780684803357', 'publication_date': date(1940, 10, 21), 'pages': 471, 'price': Decimal('15.99')},
            {'title': 'The Garden of Eden', 'author': 'Ernest Hemingway', 'isbn': '9780684802800', 'publication_date': date(1986, 5, 1), 'pages': 247, 'price': Decimal('12.25')},
            {'title': 'A Moveable Feast', 'author': 'Ernest Hemingway', 'isbn': '9780684824994', 'publication_date': date(1964, 5, 1), 'pages': 211, 'price': Decimal('11.75')},

            # George Orwell books
            {'title': '1984', 'author': 'George Orwell', 'isbn': '9780452284234', 'publication_date': date(1949, 6, 8), 'pages': 328, 'price': Decimal('13.99')},
            {'title': 'Animal Farm', 'author': 'George Orwell', 'isbn': '9780452284241', 'publication_date': date(1945, 8, 17), 'pages': 112, 'price': Decimal('9.99')},
            {'title': 'Homage to Catalonia', 'author': 'George Orwell', 'isbn': '9780156421171', 'publication_date': date(1938, 4, 25), 'pages': 232, 'price': Decimal('12.50')},
            {'title': 'Down and Out in Paris and London', 'author': 'George Orwell', 'isbn': '9780156262248', 'publication_date': date(1933, 1, 9), 'pages': 230, 'price': Decimal('11.99')},
            {'title': 'Burmese Days', 'author': 'George Orwell', 'isbn': '9780156148504', 'publication_date': date(1934, 10, 25), 'pages': 300, 'price': Decimal('12.75')},

            # J.D. Salinger books
            {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'isbn': '9780316769174', 'publication_date': date(1951, 7, 16), 'pages': 234, 'price': Decimal('11.99')},
            {'title': 'Nine Stories', 'author': 'J.D. Salinger', 'isbn': '9780316769501', 'publication_date': date(1953, 4, 6), 'pages': 198, 'price': Decimal('10.99')},
            {'title': 'Franny and Zooey', 'author': 'J.D. Salinger', 'isbn': '9780316769495', 'publication_date': date(1961, 9, 14), 'pages': 201, 'price': Decimal('11.50')},
            {'title': 'Raise High the Roof Beam, Carpenters', 'author': 'J.D. Salinger', 'isbn': '9780316769020', 'publication_date': date(1963, 1, 28), 'pages': 108, 'price': Decimal('9.50')},

            # Harper Lee books
            {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'isbn': '9780061120084', 'publication_date': date(1960, 7, 11), 'pages': 376, 'price': Decimal('12.99')},
            {'title': 'Go Set a Watchman', 'author': 'Harper Lee', 'isbn': '9780062409851', 'publication_date': date(2015, 7, 14), 'pages': 278, 'price': Decimal('13.50')},
        ]

        conditions = ['new', 'like_new', 'good', 'fair', 'poor']
        languages = ['en', 'en', 'en', 'en', 'en']  # Mostly English, but could vary

        author_dict = {author.name: author for author in authors}

        books_created = 0
        isbn_counter = 1000  # Counter to ensure unique ISBNs
        
        for book_data in books_data:
            # Generate unique ISBNs by adding variation
            base_isbn = book_data['isbn']
            # Create multiple copies of some books with different conditions
            num_copies = random.randint(1, 3) if books_created < 50 else 1
            
            for copy_num in range(num_copies):
                # Generate unique ISBN for each copy
                if copy_num > 0:
                    # Create a unique ISBN by modifying the last few digits
                    isbn_digits = list(base_isbn)
                    # Use counter to ensure uniqueness
                    counter_str = str(isbn_counter)[-3:]  # Last 3 digits of counter
                    # Replace last 3 digits (before check digit) with counter
                    for i, digit in enumerate(counter_str):
                        if len(isbn_digits) - 2 - i >= 0:
                            isbn_digits[len(isbn_digits) - 2 - i] = digit
                    isbn = ''.join(isbn_digits)
                    isbn_counter += 1
                else:
                    # For first copy, use base ISBN but ensure uniqueness
                    if Book.objects.filter(isbn=base_isbn).exists():
                        isbn_digits = list(base_isbn)
                        counter_str = str(isbn_counter)[-3:]
                        for i, digit in enumerate(counter_str):
                            if len(isbn_digits) - 2 - i >= 0:
                                isbn_digits[len(isbn_digits) - 2 - i] = digit
                        isbn = ''.join(isbn_digits)
                        isbn_counter += 1
                    else:
                        isbn = base_isbn

                # Randomize some attributes
                condition = random.choice(conditions)
                # Adjust price based on condition
                price_multiplier = {
                    'new': 1.0,
                    'like_new': 0.85,
                    'good': 0.70,
                    'fair': 0.50,
                    'poor': 0.30
                }
                price = book_data['price'] * Decimal(str(price_multiplier[condition]))
                price = price.quantize(Decimal('0.01'))

                # Random seller
                seller = random.choice(users)

                # Random editorial
                editorial = random.choice(editorials)

                # Check if book with this ISBN already exists
                if not Book.objects.filter(isbn=isbn).exists():
                    book, created = Book.objects.get_or_create(
                        isbn=isbn,
                        defaults={
                            'title': book_data['title'],
                            'author': author_dict[book_data['author']],
                            'editorial': editorial,
                            'seller': seller,
                            'publication_date': book_data['publication_date'],
                            'price': price,
                            'condition': condition,
                            'pages': book_data['pages'],
                            'language': random.choice(languages),
                            'is_available': True,
                            'description': f'A classic {book_data["title"]} by {book_data["author"]}. Condition: {condition}.'
                        }
                    )
                    if created:
                        books_created += 1
                        if books_created <= 5 or books_created % 10 == 0:
                            self.stdout.write(f'Created book {books_created}: {book.title}')

        self.stdout.write(self.style.SUCCESS(f'Created {books_created} books total'))

