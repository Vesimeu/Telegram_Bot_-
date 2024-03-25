import sqlite3

def clear_user_database(user_id, db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Удаляем запись пользователя из базы данных
    cursor.execute('''DELETE FROM users WHERE user_id = ?''', (user_id,))
    connection.commit()

    connection.close()

if __name__ == "__main__":
    user_id = '708969494'
    database_name = "database.db"  # Путь к базе данных

    clear_user_database(user_id, database_name)
