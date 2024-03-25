import sqlite3

class DatabaseHandler:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER PRIMARY KEY,
                                municipal_code TEXT,
                                stage_1_link TEXT,
                                stage_2_link TEXT,
                                stage_4_link TEXT,
                                stage_5_link TEXT,
                                points INTEGER DEFAULT 0
                                )''')
        self.connection.commit()

    def add_user(self, user_id, municipal_code):
        self.cursor.execute('''INSERT INTO users (user_id, municipal_code)
                               VALUES (?, ?)''', (user_id, municipal_code))
        self.connection.commit()

    def update_link(self, user_id, stage, link):
        stage_column = f'stage_{stage}_link'
        self.cursor.execute(f'''UPDATE users
                                 SET {stage_column} = ?
                                 WHERE user_id = ?''', (link, user_id))
        self.connection.commit()

    def update_points(self, user_id, points):
        self.cursor.execute('''UPDATE users
                               SET points = ?
                               WHERE user_id = ?''', (points, user_id))
        self.connection.commit()

    def get_user(self, user_id):
        self.cursor.execute('''SELECT * FROM users
                               WHERE user_id = ?''', (user_id,))
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()
