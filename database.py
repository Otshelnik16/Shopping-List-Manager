import sqlite3

def init_db():
    """Инициализация базы данных: создание файла shopping.db и таблицы shopping_items."""
    conn = sqlite3.connect('shopping.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shopping_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,          -- Название товара
            quantity INTEGER NOT NULL,   -- Количество
            is_purchased INTEGER DEFAULT 0  -- Статус (0 - не куплен, 1 - куплен)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Устанавливает соединение с базой данных и включает доступ к полям по именам."""
    conn = sqlite3.connect('shopping.db')
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == '__main__':
    init_db()
    print("База данных shopping.db успешно инициализирована.")
