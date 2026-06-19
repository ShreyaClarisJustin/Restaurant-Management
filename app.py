# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)






from flask import Flask, render_template
from flask import request

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

# @app.route('/login')
# def login():
#     return render_template('login.html')



from flask import request, redirect, url_for
from flask import session

app.secret_key = "your_secret_key"

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        sql = """
        SELECT * FROM users
        WHERE email=%s AND password=%s
        """

        cursor.execute(sql, (email, password))

        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect('/menu')
        else:
            return "Invalid Email or Password"

    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

# from flask import request

@app.route('/register', methods=['POST'])
def register_user():

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']

    sql = """
    INSERT INTO users(name,email,phone,password)
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(sql, (name,email,phone,password))
    db.commit()

    return render_template('login.html')

# @app.route('/admin')
# def admin():

#     cursor.execute("SELECT * FROM orders")
#     orders = cursor.fetchall()

#     return render_template(
#         'admin.html',
#         orders=orders
#     )

# @app.route('/order/<int:food_id>')
# def order(food_id):

#     cursor.execute(
#         "SELECT * FROM foods WHERE id=%s",
#         (food_id,)
#     )

#     food = cursor.fetchone()

#     return render_template(
#         'order.html',
#         food=food
#     )
@app.route('/profile')
def profile():

    if 'user_id' not in session:
        return redirect('/login')

    cursor.execute(
        """
        SELECT name,email,phone
        FROM users
        WHERE id=%s
        """,
        (session['user_id'],)
    )

    user = cursor.fetchone()

    return render_template(
        'profile.html',
        user=user
    )

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

@app.route('/admin')
def admin():

    # Total Orders
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    # Total Revenue
    cursor.execute("SELECT SUM(total_price) FROM orders")
    revenue = cursor.fetchone()[0]

    if revenue is None:
        revenue = 0

    # Total Customers
    cursor.execute("SELECT COUNT(*) FROM users")
    total_customers = cursor.fetchone()[0]

    # Most Ordered Food
    cursor.execute("""
        SELECT f.name, COUNT(*) AS order_count
        FROM orders o
        JOIN foods f
        ON o.food_id = f.id
        GROUP BY f.name
        ORDER BY order_count DESC
        LIMIT 1
    """)

    most_ordered = cursor.fetchone()

    if most_ordered:
        food_name = most_ordered[0]
        food_count = most_ordered[1]
    else:
        food_name = "No Orders Yet"
        food_count = 0

    return render_template(
        "admin.html",
        total_orders=total_orders,
        revenue=revenue,
        total_customers=total_customers,
        food_name=food_name,
        food_count=food_count
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

from flask import session

# @app.route('/history')
# def history():

#     if 'user_id' not in session:
#         return redirect('/login')

#     cursor.execute(
#         """
#         SELECT food_name,
#                quantity,
#                total_price,
#                payment_method
#         FROM orders
#         WHERE user_id=%s
#         """,
#         (session['user_id'],)
#     )

#     orders = cursor.fetchall()

#     return render_template(
#         'history.html',
#         orders=orders
#     )

@app.route('/history')
def history():

    if 'user_id' not in session:
        return redirect('/login')

    cursor.execute(
        """
        SELECT o.id,
               f.name,
               o.quantity,
               o.total_price,
               o.order_status,
               o.order_date
        FROM orders o
        JOIN foods f
        ON o.food_id = f.id
        WHERE o.user_id = %s
        ORDER BY o.order_date DESC
        """,
        (session['user_id'],)
    )

    orders = cursor.fetchall()

    return render_template(
        'history.html',
        orders=orders
    )


@app.route('/place_order', methods=['POST'])
def place_order():

    if 'user_id' not in session:
        return redirect('/login')

    food_id = request.form['food_id']
    quantity = int(request.form['quantity'])
    payment_method = request.form['payment_method']

    cursor.execute(
        "SELECT name, price FROM foods WHERE id=%s",
        (food_id,)
    )

    food = cursor.fetchone()

    food_name = food[0]
    price = food[1]

    total_price = price * quantity

    cursor.execute(
        """
        INSERT INTO orders
        (
            customer_name,
            quantity,
            total_price,
            payment_method,
            food_id,
            user_id
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (
            session['user_name'],
            quantity,
            total_price,
            payment_method,
            food_id,
            session['user_id']
        )
    )

    db.commit()

    return redirect('/success')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)