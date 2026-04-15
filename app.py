# import sqlite3
# from flask import Flask, render_template, request, redirect, url_for
# from collections import defaultdict
# from datetime import datetime
# from flask import session
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)


# app.secret_key = "abcxyz"

# # 🔹 Create Database + Table
# def init_db():
#     conn = sqlite3.connect('expenses.db')
#     cursor = conn.cursor()

#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT UNIQUE,
#         password TEXT
#     )
#     ''')

#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS expenses (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         category TEXT,
#         amount INTEGER,
#         date TEXT
#     )
#     ''')

#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS earnings (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     source TEXT,
#     amount INTEGER,
#     date TEXT
# )
#                        ''')
    


#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS savings (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     goal_name TEXT,
#     target_amount INTEGER,
#     saved_amount INTEGER
# )
#                        ''')
    
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS settings (
#     id INTEGER PRIMARY KEY,
#     monthly_budget INTEGER
# )
#                        ''')
    


#     conn.commit()
#     conn.close()

# init_db()

# # 🔹 Home Page
# @app.route('/')
# def home():

#     if 'user' not in session:
#         return redirect('/login')
    
#     # 🔹 Fetch savings goals
#     conn = sqlite3.connect('expenses.db')
#     cursor = conn.cursor()

#     cursor.execute("SELECT id, category, amount, date FROM expenses")
#     data = cursor.fetchall()

#     cursor.execute("SELECT * FROM savings")
#     goals = cursor.fetchall()

#     cursor.execute("SELECT * FROM earnings")
#     income_data = cursor.fetchall()

#     cursor.execute("SELECT SUM(amount) FROM expenses")
#     total_expenses = cursor.fetchone()[0] or 0

#     cursor.execute("SELECT SUM(amount) FROM earnings")
#     total_income = cursor.fetchone()[0] or 0

#     transactions = []

#     # Add expenses
#     for e in data:
#         transactions.append(("Expense", e[0], e[1], e[2], e[3]))
#         # ("Expense", id, category, amount, date)

#     # Add income
#     for i in income_data:
#         transactions.append(("Income", i[0], i[1], i[2], i[3]))
#         # ("Income", id, source, amount, date)

#     # Sort by date (latest first)
#     transactions.sort(key=lambda x: x[4], reverse=True)

# #  # 🔹 Monthly Total
# #     current_month = datetime.now().strftime("%Y-%m")
# #     monthly_total = 0

# #     for row in data:
# #         if row[3].startswith(current_month):
# #             monthly_total += int(row[2])


#  # 🔹 Monthly total
#     current_month = datetime.now().strftime("%Y-%m")
#     monthly_total = sum(int(row[2]) for row in data if row[3].startswith(current_month))



#  # 🔹 Budget Logic
#     # 🔹 Get budget from DB
#     cursor.execute("SELECT monthly_budget FROM settings WHERE id = 1")
#     result = cursor.fetchone()

#     if result:
#         BUDGET_LIMIT = int(result[0])
#     else:
#         BUDGET_LIMIT = 5000

#     # 🔹 Warning logic 
#     warning = None      

#     if monthly_total > BUDGET_LIMIT:
#         warning = "⚠️ Budget Exceeded!"
#     elif monthly_total > 0.8 * BUDGET_LIMIT:
#         warning = "⚠️ Approaching Budget Limit"


#     # 🔹 Chart Data
#     category_data = defaultdict(int)
#     for row in data:
#         category = row[1]
#         amount = int(row[2])
#         category_data[category] += amount

#     labels = list(category_data.keys())
#     values = list(category_data.values())

#     conn.close()


   
#     return render_template(
#     "index.html",
#     transactions=transactions,
#     total_income=total_income,
#     labels=labels,
#     values=values,
#     monthly_total=monthly_total,
#     budget=BUDGET_LIMIT,
#     warning=warning,
#     goals=goals,
#     # total_savings=total_savings,
#     total_expenses=total_expenses
# )

# # 🔹 Add Expense
# @app.route('/add', methods=['POST'])
# def add():
#     category = request.form['category']
#     amount = request.form['amount']
#     date = datetime.now().strftime("%Y-%m-%d")

#     conn = sqlite3.connect('expenses.db')
#     cursor = conn.cursor()

#     cursor.execute(
#         "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
#         (category, amount, date)
#     )

#     conn.commit()
#     conn.close()

#     return redirect(url_for('home'))

# # 🔹 Delete Expense
# @app.route('/delete/<int:id>', methods=['POST'])
# def delete(id):
#     conn = sqlite3.connect('expenses.db')
#     cursor = conn.cursor()

#     cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
#     conn.commit()
#     conn.close()

#     return redirect(url_for('home'))


# # 🔹 Delete Income
# @app.route('/delete_income/<int:id>', methods=['POST'])
# def delete_income(id):
#     conn = sqlite3.connect('expenses.db')
#     cursor = conn.cursor()

#     cursor.execute("DELETE FROM earnings WHERE id = ?", (id,))
#     conn.commit()
#     conn.close()

#     return redirect(url_for('home'))

# # 🔹 Edit Page
# @app.route('/edit/<int:id>')
# def edit(id):
#     conn = sqlite3.connect('expenses.db')
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM expenses WHERE id = ?", (id,))
#     expense = cursor.fetchone()

#     conn.close()

#     return render_template("edit.html", expense=expense)

# # 🔹 Update Expense
# @app.route('/update/<int:id>', methods=['POST'])
# def update(id):
#     category = request.form['category']
#     amount = request.form['amount']

#     conn = sqlite3.connect('expenses.db')
#     cursor = conn.cursor()

#     cursor.execute(
#         "UPDATE expenses SET category = ?, amount = ? WHERE id = ?",
#         (category, amount, id)
#     )

#     conn.commit()
#     conn.close()

#     return redirect(url_for('home'))


# @app.route('/add_income', methods=['POST'])
# def add_income():
#     source = request.form['source']
#     amount = request.form['amount']
#     date = datetime.now().strftime("%Y-%m-%d")

#     conn = sqlite3.connect('expenses.db')
#     cursor = conn.cursor()

#     cursor.execute(
#         "INSERT INTO earnings (source, amount, date) VALUES (?, ?, ?)",
#         (source, amount, date)
#     )

#     conn.commit()
#     conn.close()

#     return redirect('/')


# @app.route('/add_goal', methods=['POST'])
# def add_goal():
#     name = request.form['goal_name']
#     target = request.form['target_amount']

#     conn = sqlite3.connect('expenses.db')
#     cursor = conn.cursor()

#     cursor.execute(
#         "INSERT INTO savings (goal_name, target_amount, saved_amount) VALUES (?, ?, 0)",
#         (name, target)
#     )

#     conn.commit()
#     conn.close()

#     return redirect('/')


# @app.route('/add_to_goal/<int:id>', methods=['POST'])
# def add_to_goal(id):
#     amount = int(request.form['amount'])

#     conn = sqlite3.connect('expenses.db')
#     cursor = conn.cursor()

#     cursor.execute(
#         "UPDATE savings SET saved_amount = saved_amount + ? WHERE id = ?",
#         (amount, id)
#     )

#     conn.commit()
#     conn.close()

#     return redirect('/')



# @app.route('/set_budget', methods=['POST'])
# def set_budget():
#     budget = request.form['budget']

#     conn = sqlite3.connect('expenses.db')
#     cursor = conn.cursor()

#     # Insert or update
#     cursor.execute("""
#         INSERT INTO settings (id, monthly_budget)
#         VALUES (1, ?)
#         ON CONFLICT(id) DO UPDATE SET monthly_budget=excluded.monthly_budget
#     """, (budget,))

#     conn.commit()
#     conn.close()

#     return redirect('/')


# #signup
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = generate_password_hash(request.form['password'])

#         conn = sqlite3.connect('expenses.db')
#         cursor = conn.cursor()

#         try:
#             cursor.execute(
#                 "INSERT INTO users (username, password) VALUES (?, ?)",
#                 (username, password)
#             )
#             conn.commit()
#         except:
#             return "⚠️ User already exists!"

#         conn.close()
#         return redirect('/login')

#     return render_template('signup.html')



# #login
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         conn = sqlite3.connect('expenses.db')
#         cursor = conn.cursor()

#         cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
#         user = cursor.fetchone()

#         conn.close()

#         if user and check_password_hash(user[2], password):
#             session['user'] = user[1]
#             return redirect('/')
#         else:
#             return "❌ Invalid credentials"

#     return render_template('login.html')



# #logout
# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect('/login')


# if __name__ == '__main__':
#     import os
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)


import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from collections import defaultdict
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ✅ FIX 2: Secret key from environment variable
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret")

# ✅ FIX 1: Stable DB path (fixes Render SQLite persistence issues)
DB_PATH = os.path.join(os.getcwd(), "expenses.db")


def get_db():
    """Helper: returns a connection with safe threading for Render."""
    # ✅ FIX 5: check_same_thread=False for concurrent requests
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# ─── Init DB ──────────────────────────────────────────────────────────────────
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            amount   INTEGER,
            date     TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS earnings (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            amount INTEGER,
            date   TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS savings (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_name     TEXT,
            target_amount INTEGER,
            saved_amount  INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id             INTEGER PRIMARY KEY,
            monthly_budget INTEGER
        )
    ''')

    conn.commit()
    conn.close()


init_db()


# ─── Home ─────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    # ✅ FIX 4: session protection
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT id, category, amount, date FROM expenses")
        data = cursor.fetchall()

        cursor.execute("SELECT * FROM savings")
        goals = cursor.fetchall()

        cursor.execute("SELECT * FROM earnings")
        income_data = cursor.fetchall()

        cursor.execute("SELECT SUM(amount) FROM expenses")
        total_expenses = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(amount) FROM earnings")
        total_income = cursor.fetchone()[0] or 0

        cursor.execute("SELECT monthly_budget FROM settings WHERE id = 1")
        result = cursor.fetchone()
        BUDGET_LIMIT = int(result[0]) if result else 5000

        conn.close()
    except Exception as e:
        print("DB Error in home():", e)
        return "Internal Server Error — check logs", 500

    # Build unified transaction list
    transactions = []
    for e in data:
        transactions.append(("Expense", e[0], e[1], e[2], e[3]))
    for i in income_data:
        transactions.append(("Income", i[0], i[1], i[2], i[3]))
    transactions.sort(key=lambda x: x[4], reverse=True)

    # Monthly total
    current_month = datetime.now().strftime("%Y-%m")
    monthly_total = sum(int(row[2]) for row in data if row[3].startswith(current_month))

    # Warning logic
    warning = None
    if monthly_total > BUDGET_LIMIT:
        warning = "⚠️ Budget Exceeded!"
    elif monthly_total > 0.8 * BUDGET_LIMIT:
        warning = "⚠️ Approaching Budget Limit"

    # Chart data
    category_data = defaultdict(int)
    for row in data:
        category_data[row[1]] += int(row[2])
    labels = list(category_data.keys())
    values = list(category_data.values())

    return render_template(
        "index.html",
        transactions=transactions,
        total_income=total_income,
        labels=labels,
        values=values,
        monthly_total=monthly_total,
        budget=BUDGET_LIMIT,
        warning=warning,
        goals=goals,
        total_expenses=total_expenses
    )


# ─── Add Expense ──────────────────────────────────────────────────────────────
@app.route('/add', methods=['POST'])
def add():
    # ✅ FIX 4: session protection
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        category = request.form['category']
        amount = request.form['amount']
        date = datetime.now().strftime("%Y-%m-%d")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
            (category, amount, date)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB Error in add():", e)

    # ✅ FIX 3: consistent redirect
    return redirect(url_for('home'))


# ─── Delete Expense ───────────────────────────────────────────────────────────
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB Error in delete():", e)

    return redirect(url_for('home'))


# ─── Delete Income ────────────────────────────────────────────────────────────
@app.route('/delete_income/<int:id>', methods=['POST'])
def delete_income(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM earnings WHERE id = ?", (id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB Error in delete_income():", e)

    return redirect(url_for('home'))


# ─── Edit Expense Page ────────────────────────────────────────────────────────
@app.route('/edit/<int:id>')
def edit(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (id,))
        expense = cursor.fetchone()
        conn.close()
    except Exception as e:
        print("DB Error in edit():", e)
        return redirect(url_for('home'))

    return render_template("edit.html", expense=expense)


# ─── Update Expense ───────────────────────────────────────────────────────────
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        category = request.form['category']
        amount = request.form['amount']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE expenses SET category = ?, amount = ? WHERE id = ?",
            (category, amount, id)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB Error in update():", e)

    return redirect(url_for('home'))


# ─── Add Income ───────────────────────────────────────────────────────────────
@app.route('/add_income', methods=['POST'])
def add_income():
    # ✅ FIX 4: session protection
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        source = request.form['source']
        amount = request.form['amount']
        date = datetime.now().strftime("%Y-%m-%d")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO earnings (source, amount, date) VALUES (?, ?, ?)",
            (source, amount, date)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB Error in add_income():", e)

    return redirect(url_for('home'))


# ─── Add Savings Goal ─────────────────────────────────────────────────────────
@app.route('/add_goal', methods=['POST'])
def add_goal():
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        name = request.form['goal_name']
        target = request.form['target_amount']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO savings (goal_name, target_amount, saved_amount) VALUES (?, ?, 0)",
            (name, target)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB Error in add_goal():", e)

    return redirect(url_for('home'))


# ─── Add to Savings Goal ──────────────────────────────────────────────────────
@app.route('/add_to_goal/<int:id>', methods=['POST'])
def add_to_goal(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        amount = int(request.form['amount'])

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE savings SET saved_amount = saved_amount + ? WHERE id = ?",
            (amount, id)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB Error in add_to_goal():", e)

    return redirect(url_for('home'))


# ─── Set Budget ───────────────────────────────────────────────────────────────
@app.route('/set_budget', methods=['POST'])
def set_budget():
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        budget = request.form['budget']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO settings (id, monthly_budget)
            VALUES (1, ?)
            ON CONFLICT(id) DO UPDATE SET monthly_budget=excluded.monthly_budget
        """, (budget,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB Error in set_budget():", e)

    return redirect(url_for('home'))


# ─── Signup ───────────────────────────────────────────────────────────────────
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print("Signup error:", e)
            return "⚠️ User already exists!"

        return redirect(url_for('login'))

    return render_template('signup.html')


# ─── Login ────────────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            conn.close()
        except Exception as e:
            print("Login DB error:", e)
            return "Internal error — try again", 500

        if user and check_password_hash(user[2], password):
            session['user'] = user[1]
            return redirect(url_for('home'))
        else:
            return "❌ Invalid credentials"

    return render_template('login.html')


# ─── Logout ───────────────────────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
