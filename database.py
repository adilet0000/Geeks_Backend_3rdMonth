import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    date DATE NOT NULL,
                    food_rating INTEGER NOT NULL,
                    cleanliness_rating INTEGER NOT NULL,
                    extra_comments TEXT
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS dishes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL,
                    description TEXT NOT NULL,
                    image_path TEXT
                )
            ''')
            conn.commit()

    def save_review(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT INTO reviews (name, contact, date, food_rating, cleanliness_rating, extra_comments)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    data['name'],
                    data['contact'],
                    data['date'],
                    data['food_rating'],
                    data['cleanliness_rating'],
                    data['extra_comments']
                )
            )
            conn.commit()

    def save_dish(self, dish: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT INTO dishes (name, category, price, description, image_path)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    dish['name'],
                    dish['category'],
                    dish['price'],
                    dish['description'],
                    dish['image_path']
                )
            )
            conn.commit()

    def get_dishes(self, sort_by: str = "name"):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            query = f"SELECT name, category, price, description, image_path FROM dishes ORDER BY {sort_by} ASC"
            cursor.execute(query)
            return cursor.fetchall()
