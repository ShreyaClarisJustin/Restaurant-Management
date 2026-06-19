# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)






from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sandra",
    database="restaurant_db"
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():

    cursor.execute("SELECT * FROM foods")
    foods = cursor.fetchall()

    return render_template(
        'menu.html',
        foods=foods
    )

@app.route('/admin')
def admin():

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    return render_template(
        'admin.html',
        orders=orders
    )

@app.route('/order/<int:food_id>')
def order(food_id):

    cursor.execute(
        "SELECT * FROM foods WHERE id=%s",
        (food_id,)
    )

    food = cursor.fetchone()

    return render_template(
        'order.html',
        food=food
    )

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)