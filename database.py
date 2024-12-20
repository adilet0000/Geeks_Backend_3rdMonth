import sqlite3

class Database:
    def __init__(self, path:str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS poll (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    waiting_for_name TEXT,
                    waiting_for_contact INTEGER,
                    waiting_for_date DATE,
                    waiting_for_food_rating INTEGER,
                    waiting_for_cleanliness_rating INTEGER,
                    waiting_for_extra_comments TEXT
                )
            ''')
            conn.commit()


    def save_poll(self, data:dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                    INSERT INTO poll (waiting_for_name, waiting_for_contact, waiting_for_date, waiting_for_food_rating, waiting_for_cleanliness_rating, waiting_for_extra_comments)
                    VALUES(?, ?, ?, ?, ?, ?)
                """,
                (data['waiting_for_name'], data['waiting_for_contact'], data['waiting_for_date'], data['waiting_for_food_rating'], data['waiting_for_cleanliness_rating'], data['waiting_for_extra_comments'])
            )
