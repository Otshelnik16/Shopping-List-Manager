from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

# 3.1 Функция index()
@app.route('/')
def index():
    conn = database.get_db_connection()
    # Запрашиваем все привычки из таблицы habits
    habits = conn.execute('SELECT * FROM habits ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', habits=habits)

# 3.2 Функция add_habit()
@app.route('/add', methods=['POST'])
def add_habit():
    title = request.form['title']
    goal = request.form['goal']
    
    conn = database.get_db_connection()
    # Вставляем новую привычку в БД
    conn.execute('INSERT INTO habits (title, goal) VALUES (?, ?)', 
                 (title, goal))
    conn.commit()
    conn.close()
    # После добавления возвращаемся на главную
    return redirect(url_for('index'))

# 3.3 Функция delete_habit()
@app.route('/delete/<int:id>')
def delete_habit(id):
    conn = database.get_db_connection()
    # Удаляем привычку по ID
    conn.execute('DELETE FROM habits WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    # После удаления возвращаемся на главную
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
