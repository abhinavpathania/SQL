import sqlite3

def clear_database():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # Clear data from the Borrowers table
        cursor.execute('DELETE FROM Borrowers')

        # Clear data from the Transactions table
        cursor.execute('DELETE FROM Transactions')
        
        # Clear data from the Books table
        cursor.execute('DELETE FROM Books')



        # Commit the changes
        conn.commit()
        print('Database cleared successfully.')

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    clear_database()
