from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

@app.route('/')
def index():
    """Главная страница: отображает список всех товаров."""
    conn = database.get_db_connection()
    items = conn.execute('SELECT * FROM shopping_items ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    """Добавляет новый товар в список покупок."""
    name = request.form['name']
    quantity = request.form['quantity']
    
    conn = database.get_db_connection()
    conn.execute('INSERT INTO shopping_items (name, quantity) VALUES (?, ?)',
                 (name, quantity))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/purchase/<int:item_id>')
def purchase_item(item_id):
    """Отмечает товар как купленный."""
    conn = database.get_db_connection()
    conn.execute('UPDATE shopping_items SET is_purchased = 1 WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    """Удаляет товар из списка."""
    conn = database.get_db_connection()
    conn.execute('DELETE FROM shopping_items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
