import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_tables(conn):
    try:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS Concerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TIMESTAMP NOT NULL,
            available_tickets INTEGER NOT NULL
        );
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS Tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL CHECK(status IN ('reserved', 'purchased', 'canceled')),
            user_id INTEGER NOT NULL,
            concert_id INTEGER NOT NULL,
            reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cancellation_date TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users (id),
            FOREIGN KEY (concert_id) REFERENCES Concerts (id)
        );
        ''')

        conn.commit()
        print("Tables created successfully.")
    
    except Error as e:
        print(f"Error creating tables: {e}")

def insert_initial_data(conn):
    try:
        c = conn.cursor()

        c.execute("INSERT OR IGNORE INTO Users (name, email) VALUES ('Juan arez', 'juan.arez@email.com')")
        c.execute("INSERT OR IGNORE INTO Users (name, email) VALUES ('Ana mez', 'ana.mez@email.com')")

        c.execute("INSERT OR IGNORE INTO Concerts (name, date, available_tickets) VALUES ('Concert A', '2024-12-15 20:00:00', 100)")
        c.execute("INSERT OR IGNORE INTO Concerts (name, date, available_tickets) VALUES ('Concert B', '2024-12-20 21:00:00', 150)")

        c.execute("INSERT OR IGNORE INTO Tickets (status, user_id, concert_id) VALUES ('purchased', 1, 1)")
        c.execute("INSERT OR IGNORE INTO Tickets (status, user_id, concert_id) VALUES ('reserved', 2, 2)")

        conn.commit()
        print("Initial data inserted successfully.")
    
    except Error as e:
        print(f"Error inserting data: {e}")

def main():
    database = "tickets_concerts.db"
    conn = create_connection(database)
    if conn:
        create_tables(conn)
        insert_initial_data(conn)
        conn.close()

if __name__ == '__main__':
    main()
