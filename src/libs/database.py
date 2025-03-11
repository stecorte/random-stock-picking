import os 
import sqlite3

def create_db_if_not_exists():
    if not os.path.exists("database"):
        os.makedirs("database")
        print("'database' folder created successfully")

    db_path = os.path.join("database", "stocks_history.db")
    
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        print(f"Database connected on: {db_path}")

        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY,
            stock TEXT NOT NULL,
            stock_date DATE NOT NULL,
            close_price REAL NOT NULL,
            UNIQUE(stock, stock_date)        
        )
        ''')
        conn.commit()
        print("'history' table created")
    
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")

    finally:
        if conn:
            conn.close()


def store_stock_history(ticker, stock_history):
    conn = sqlite3.connect("database/stocks_history.db")
    cursor = conn.cursor()

    query = """
    INSERT OR IGNORE INTO history (stock, start_date, close_price) VALUES (?, ?, ?)
    """

    data_to_insert = []
    for stock_date, stock_data in stock_history.iterrows():
        data_to_insert.append((ticker, stock_date.date(), stock_data['Close']))

    try:
        cursor.executemany(query, stock_history)
        conn.commit()
    
    except sqlite3.Error as e:
        print(f"Error on insert: {e}")
        conn.rollback()
    
    finally:
        conn.close()


def get_stock_history(stock, since):
    conn = sqlite3.connect("database/stocks_history.db")
    cursor = conn.cursor()

    query = """
    SELECT stock, stock_date, close_price
    FROM history 
    WHERE stock = ? AND stock_date >= ? AND stock_date <= date(?, '+1 year') 
    ORDER BY stock_date ASC
    """

    try:
        cursor.execute(query, (stock, since))
        results = cursor.fetchall()

        stock_history = []
        for row in results:
            stock_history.append({
                'stock': row[0],
                'stock_date': row[1],
                'close_price': row[2]
            })

        return stock_history
    
    except sqlite3.Error as e:
        print(f"Error on fetching history from the db: {e}")
        return []
    
    finally:
        conn.close()