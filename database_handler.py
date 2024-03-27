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
                                institution_name TEXT,
                                full_name TEXT,
                                stage_1_link TEXT,
                                stage_2_link TEXT,
                                stage_4_link TEXT,
                                stage_5_link TEXT,
                                stage_6_link TEXT,
                                points INTEGER DEFAULT 0
                                )''')
        self.connection.commit()

    def update_full_name(self, user_id, full_name):
        self.cursor.execute('''UPDATE users
                               SET full_name = ?
                               WHERE user_id = ?''', (full_name, user_id))
        self.connection.commit()

    def update_institution_name(self, user_id, institution_name):
        self.cursor.execute('''UPDATE users
                               SET institution_name = ?
                               WHERE user_id = ?''', (institution_name, user_id))
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

    def is_user_registered(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        return self.cursor.fetchone() is not None

    def add_video_link(self, user_id, link):
        self.cursor.execute('''UPDATE users
                               SET stage_1_link = ?
                               WHERE user_id = ?''', (link, user_id))
        self.connection.commit()

    def add_photo_link(self, user_id, link):
        self.cursor.execute('''UPDATE users
                               SET stage_2_link = ?
                               WHERE user_id = ?''', (link, user_id))
        self.connection.commit()

    def add_answer(self, user_id, answer):
        self.cursor.execute('''UPDATE users
                               SET stage_6_link = ?
                               WHERE user_id = ?''', (answer, user_id))
        self.connection.commit()

    def add_points(self, user_id, points):
        user = self.get_user(user_id)
        current_points = user[9] if user else 0
        current_points = int(current_points) if current_points else 0  # Преобразуем в целое число, если возможно
        new_points = current_points + points
        self.cursor.execute('''UPDATE users
                               SET points = ?
                               WHERE user_id = ?''', (new_points, user_id))
        self.connection.commit()

    def add_presentation_link(self, user_id, link):
        self.cursor.execute('''UPDATE users
                               SET stage_4_link = ?
                               WHERE user_id = ?''', (link, user_id))
        self.connection.commit()

    def add_social_link(self, user_id, link):
        self.cursor.execute('''UPDATE users
                               SET stage_5_link = ?
                               WHERE user_id = ?''', (link, user_id))
        self.connection.commit()

    def close(self):
        self.connection.close()
