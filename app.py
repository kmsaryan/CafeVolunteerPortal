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
    return render_template("home.html")

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
        shift_time = request.form['shift-time']
        start_time, end_time = shift_time.split('-')

        # Calculate duration
        start_time_dt = datetime.strptime(start_time.strip(), '%H:%M')
        end_time_dt = datetime.strptime(end_time.strip(), '%H:%M')
        duration = (end_time_dt - start_time_dt).seconds / 3600

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the volunteer worked on the previous day
        last_entry = cursor.execute("""
            SELECT date FROM Signups WHERE name = ? ORDER BY date DESC LIMIT 1
        """, (name,)).fetchone()

        if last_entry:
            last_date = datetime.strptime(last_entry["date"], "%Y-%m-%d")
            signup_date = datetime.strptime(date, "%Y-%m-%d")
            if (signup_date - last_date).days == 1:
                conn.close()
                return "Volunteer cannot work on consecutive days!", 400

        # Insert the new signup
        cursor.execute("""
            INSERT INTO Signups (name, date, start_time, end_time) 
            VALUES (?, ?, ?, ?)
        """, (name, date, start_time, end_time))
        conn.commit()
        conn.close()

        return redirect(url_for("view_signups"))

    return render_template("signup.html")

# Route to confirm attendance and update Credits table
@app.route("/confirm/<int:signup_id>", methods=["POST"])
def confirm_attendance(signup_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch signup details
    signup = cursor.execute("SELECT * FROM Signups WHERE id = ?", (signup_id,)).fetchone()
    if not signup:
        conn.close()
        return "Signup not found!", 404

    if signup["attendance"] == "Confirmed":
        conn.close()
        return "Attendance already confirmed!", 400

    # Calculate credits earned
    start_time = datetime.strptime(signup["start_time"], "%H:%M")
    end_time = datetime.strptime(signup["end_time"], "%H:%M")
    duration = (end_time - start_time).seconds / 3600
    amount_made = duration * 20

    # Get the last balance from the Credits table
    last_balance = cursor.execute("""
        SELECT balance FROM Credits WHERE name = ? ORDER BY date DESC LIMIT 1
    """, (signup["name"],)).fetchone()
    new_balance = (last_balance["balance"] if last_balance else 0) + amount_made

    # Update attendance and add entry to Credits
    cursor.execute("UPDATE Signups SET attendance = 'Confirmed' WHERE id = ?", (signup_id,))
    cursor.execute("""
        INSERT INTO Credits (name, date, amount_made, balance) VALUES (?, ?, ?, ?)
    """, (signup["name"], signup["date"], amount_made, new_balance))
    conn.commit()
    conn.close()

    return redirect(url_for("view_signups"))

# Route to handle debit transactions
@app.route("/debit", methods=["POST","GET"])
def add_debit():
    name = request.form["name"]
    date = request.form["date"]
    amount_spent = float(request.form["amount_spent"])

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the last balance from the Credits table
    last_balance = cursor.execute("""
        SELECT balance FROM Credits WHERE name = ? ORDER BY date DESC LIMIT 1
    """, (name,)).fetchone()
    if not last_balance or last_balance["balance"] < amount_spent:
        conn.close()
        return "Insufficient balance!", 400

    # Calculate the new balance
    new_balance = last_balance["balance"] - amount_spent

    # Add entry to Debits table
    cursor.execute("""
        INSERT INTO Debits (name, date, amount_spent, balance) VALUES (?, ?, ?, ?)
    """, (name, date, amount_spent, new_balance))
    conn.commit()
    conn.close()
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
