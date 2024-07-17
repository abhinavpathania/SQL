import sqlite3
from datetime import datetime, timedelta

# Connect to the SQLite database (or create a new one if it doesn't exist)
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create Books table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID INTEGER PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        Genre TEXT,
        ISBN TEXT,
        AvailableCopies INTEGER,
        TotalCopies INTEGER
    )
''')

# Create Borrowers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Borrowers (
        BorrowerID INTEGER PRIMARY KEY,
        Name TEXT,
        Address TEXT,
        PhoneNumber TEXT,
        Email TEXT
    )
''')

# Create Transactions table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Transactions (
        TransactionID INTEGER PRIMARY KEY,
        BookID INTEGER,
        BorrowerID INTEGER,
        BorrowDate TEXT,
        ReturnDate TEXT,
        FOREIGN KEY (BookID) REFERENCES Books(BookID),
        FOREIGN KEY (BorrowerID) REFERENCES Borrowers(BorrowerID)
    )
''')







# Commit the changes and close the connection
conn.commit()
conn.close()

# Function to borrow or return a book
def perform_transaction():
    while True:
        print("\nChoose from the following? :")
        print("1. Borrow a book")
        print("2. Return a book")
        print("3. Exit")

        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == "1":
            # Borrow a book
            book_title = input("Enter the title of the book you want to borrow: ")
            borrower_name = input("Enter your name: ")
            borrower_address = input("Enter your address: ")
            borrower_phone = input("Enter your phone number: ")
            borrower_email = input("Enter your email: ")

            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            # Check if the book is available
            cursor.execute('SELECT BookID, AvailableCopies FROM Books WHERE Title = ?', (book_title,))
            book_info = cursor.fetchone()

            if book_info and book_info[1] > 0:
                book_id = book_info[0]

                # Update the available copies
                cursor.execute('UPDATE Books SET AvailableCopies = ? WHERE BookID = ?', (book_info[1] - 1, book_id))

                # Insert borrower details
                cursor.execute('INSERT INTO Borrowers (Name, Address, PhoneNumber, Email) VALUES (?, ?, ?, ?)',
                               (borrower_name, borrower_address, borrower_phone, borrower_email))
                borrower_id = cursor.lastrowid

                # Record the transaction
                borrow_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('INSERT INTO Transactions (BookID, BorrowerID, BorrowDate, ReturnDate) VALUES (?, ?, ?, ?)',
                               (book_id, borrower_id, borrow_date, return_date))

                print(f'Book with ID {book_id} has been borrowed by Borrower ID {borrower_id}')

                # Print book details
                cursor.execute('SELECT * FROM Books WHERE BookID = ?', (book_id,))
                book_details = cursor.fetchone()
                
                print('\nBook Details:')
                print(f'BookID: {book_details[0]}')
                print(f'Title: {book_details[1]}')
                print(f'Author: {book_details[2]}')
                print(f'Genre: {book_details[3]}')
                print(f'ISBN: {book_details[4]}')
                print(f'Available Copies: {book_details[5]}')
                print(f'Total Copies: {book_details[6]}')

                # Print borrower details
                cursor.execute('SELECT * FROM Borrowers WHERE BorrowerID = ?', (borrower_id,))
                borrower_details = cursor.fetchone()

                print('\nBorrower Details:')
                print(f'BorrowerID: {borrower_details[0]}')
                print(f'Name: {borrower_details[1]}')
                print(f'Address: {borrower_details[2]}')
                print(f'Phone Number: {borrower_details[3]}')
                print(f'Email: {borrower_details[4]}')

                # Commit the changes and close the connection
                conn.commit()
                conn.close()
            else:
                print('Book not available for borrowing')
                conn.close()

        elif choice == "2":
            # Return a book
            book_id_to_return = input("Enter the ID of the book you want to return: ")
            borrower_id_to_return = input("Enter your Borrower ID: ")

            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            # Check if the book is borrowed by the given borrower
            cursor.execute('SELECT * FROM Transactions WHERE BookID = ? AND BorrowerID = ?',
                           (book_id_to_return, borrower_id_to_return))
            transaction_info = cursor.fetchone()

            if transaction_info:
                # Update the available copies
                cursor.execute('UPDATE Books SET AvailableCopies = AvailableCopies + 1 WHERE BookID = ?',
                               (book_id_to_return,))

                # Record the return date in the transaction
                return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('UPDATE Transactions SET ReturnDate = ? WHERE BookID = ? AND BorrowerID = ?',
                               (return_date, book_id_to_return, borrower_id_to_return))

                print(f'Book with ID {book_id_to_return} has been returned by Borrower ID {borrower_id_to_return}')

                # Commit the changes and close the connection
                conn.commit()
                conn.close()
            else:
                print('Book not borrowed by the given borrower or invalid Book/Borrower ID')
                conn.close()

        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break

        else:
            print('Invalid choice')

# Example usage of perform_transaction function
perform_transaction()
