from database_handler import DatabaseHandler

def main():
    db_handler = DatabaseHandler("database.db")
    users = db_handler.cursor.execute("SELECT * FROM users").fetchall()
    print("Содержимое таблицы пользователей:")
    for user in users:
        print(user)
    db_handler.close()

if __name__ == "__main__":
    main()
