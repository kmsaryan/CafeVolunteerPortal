from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

DATABASE = "db.sqlite"

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@app.route("/")
def index():
    conn = get_db_connection()
    today = datetime.now().strftime("%Y-%m-%d")
    today_signups = conn.execute("SELECT * FROM Signups WHERE date = ?", (today,)).fetchall()
    conn.close()
    return render_template("home.html", today_signups=today_signups)

# Route to view signups
@app.route("/signups")
def view_signups():
    conn = get_db_connection()
    signups = conn.execute("SELECT * FROM Signups").fetchall()
    conn.close()
    return render_template("signups.html", signups=signups)

# Route to handle signup form
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        shift_time = request.form["shift-time"]
        start_time, end_time = shift_time.split('-')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check for duplicate signups
        duplicate = cursor.execute("""
            SELECT * FROM Signups WHERE name = ? AND date = ?
        """, (name, date)).fetchone()
        if duplicate:
            conn.close()
            return render_template("signup.html", signup_message="You have already signed up for this date!")

        # Check if fewer than two workers are signed up
        worker_count = cursor.execute("""
            SELECT COUNT(*) AS count FROM Signups WHERE date = ?
        """, (date,)).fetchone()["count"]
        if worker_count >= 2:
            conn.close()
            return render_template("signup.html", signup_message="This date already has enough workers!")

        # Insert the new signup
        cursor.execute("""
            INSERT INTO Signups (name, date, start_time, end_time)
            VALUES (?, ?, ?, ?)
        """, (name, date, start_time.strip(), end_time.strip()))
        conn.commit()
        conn.close()
        return redirect(url_for("view_signups"))

    return render_template("signup.html", signup_message=None)

# Route to handle attendance confirmation and update Credits table
@app.route("/confirm", methods=["POST", "GET"])
def confirm_attendance():
    if request.method == "POST":
        name = request.form["name"]
        shift_date = request.form["shift-date"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch signup details for the given name and date
        signup = cursor.execute("""
            SELECT * FROM Signups WHERE name = ? AND date = ? LIMIT 1
        """, (name, shift_date)).fetchone()

        if not signup:
            conn.close()
            return render_template("confirm.html", confirm_message="Signup not found!")

        if signup["attendance"] == "Confirmed":
            conn.close()
            return render_template("confirm.html", confirm_message="Attendance already confirmed!")

        # Calculate credits earned
        start_time = datetime.strptime(signup["start_time"], "%H:%M")
        end_time = datetime.strptime(signup["end_time"], "%H:%M")
        duration = (end_time - start_time).seconds / 3600
        amount_made = duration * 20

        # Calculate the updated balance considering debits
        total_credits = cursor.execute("""
            SELECT COALESCE(SUM(amount_made), 0) AS total_credits FROM Credits WHERE name = ?
        """, (name,)).fetchone()["total_credits"]

        total_debits = cursor.execute("""
            SELECT COALESCE(SUM(amount_spent), 0) AS total_debits FROM Debits WHERE name = ?
        """, (name,)).fetchone()["total_debits"]

        current_balance = total_credits - total_debits + amount_made

        # Update attendance and add entry to Credits
        cursor.execute("UPDATE Signups SET attendance = 'Confirmed' WHERE id = ?", (signup["id"],))
        cursor.execute("""
            INSERT INTO Credits (name, date, amount_made, balance) VALUES (?, ?, ?, ?)
        """, (name, shift_date, amount_made, current_balance))
        conn.commit()
        conn.close()

        return render_template("confirm.html", confirm_message="Attendance confirmed successfully!")

    # GET request
    return render_template("confirm.html", confirm_message="")



@app.route("/debit", methods=["GET", "POST"])
def add_debit():
    if request.method == "POST":
        # Handle the form submission
        try:
            name = request.form["name"]
            date = request.form["date"]
            amount_spent = float(request.form["amount_spent"])
        except KeyError as e:
            return f"Missing field: {e.args[0]}", 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Calculate the updated balance considering both Credits and Debits
        total_credits = cursor.execute("""
            SELECT COALESCE(SUM(amount_made), 0) AS total_credits FROM Credits WHERE name = ?
        """, (name,)).fetchone()["total_credits"]

        total_debits = cursor.execute("""
            SELECT COALESCE(SUM(amount_spent), 0) AS total_debits FROM Debits WHERE name = ?
        """, (name,)).fetchone()["total_debits"]

        current_balance = total_credits - total_debits

        # Check if the balance is sufficient
        if current_balance < amount_spent:
            conn.close()
            return "Insufficient balance!", 400

        # Calculate the new balance
        new_balance = current_balance - amount_spent

        # Add entry to the Debits table
        cursor.execute("""
            INSERT INTO Debits (name, date, amount_spent, balance) VALUES (?, ?, ?, ?)
        """, (name, date, amount_spent, new_balance))
        conn.commit()
        conn.close()

        return redirect(url_for("view_debits"))

    # Render the debit form for a GET request
    return render_template("debit_entry.html")




# Route to view debits
@app.route("/debits")
def view_debits():
    conn = get_db_connection()
    debits = conn.execute("SELECT * FROM Debits").fetchall()
    conn.close()
    return render_template("debits.html", debits=debits)

# Route to view credits
@app.route("/credits")
def view_credits():
    conn = get_db_connection()
    credits = conn.execute("SELECT * FROM Credits").fetchall()
    conn.close()
    return render_template("credits.html", credits=credits)

if __name__ == "__main__":
    app.run(debug=True)
