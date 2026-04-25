import sqlite3

def init_db():
    """
    Инициализация базы данных: создание файла habits.db и таблицы habits.
    """
    # Указываем имя базы данных из ТЗ [cite: 13]
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    # Создаем таблицу с полями, необходимыми для работы шаблонов [cite: 15]
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,         -- Название привычки
            goal INTEGER NOT NULL,          -- Цель в днях
            streak INTEGER DEFAULT 0,       -- Текущий прогресс (дней выполнено)
            status INTEGER DEFAULT 0        -- Статус (0 - не выполнено сегодня, 1 - выполнено)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_habits():
    """Получение всех привычек из базы данных."""
    conn = sqlite3.connect('habits.db')
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к полям по именам: habit['title'] [cite: 81]
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM habits')
    habits = cursor.fetchall()
    conn.close()
    return habits

def add_habit(title, goal):
    """Добавление новой привычки в базу данных."""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    # streak и status устанавливаются в 0 по умолчанию при создании
    cursor.execute('INSERT INTO habits (title, goal) VALUES (?, ?)', (title, goal))
    conn.commit()
    conn.close()

def update_habit_status(habit_id):
    """Переключение статуса выполнения (0 <-> 1) и инкремент прогресса."""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    # Сначала получаем текущий статус и прогресс
    cursor.execute('SELECT status, streak FROM habits WHERE id = ?', (habit_id,))
    habit = cursor.fetchone()
    
    if habit:
        new_status = 1 if habit[0] == 0 else 0
        # Если статус меняется на "выполнено", увеличиваем прогресс на 1
        new_streak = habit[1] + 1 if new_status == 1 else max(0, habit[1] - 1)
        
        cursor.execute('UPDATE habits SET status = ?, streak = ? WHERE id = ?', 
                       (new_status, new_streak, habit_id))
    
    conn.commit()
    conn.close()

def delete_habit(habit_id):
    """Удаление привычки по ID."""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("База данных habits.db успешно инициализирована.")
