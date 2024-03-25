from database_handler import DatabaseHandler

def main():
    db_handler = DatabaseHandler("database.db")
    # Дополнительные операции инициализации базы данных могут быть добавлены здесь
    db_handler.close()

if __name__ == "__main__":
    main()
