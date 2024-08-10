from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Define the path to the database
db_path = "/Users/davidsmacbook/Desktop/Programming_Projects/306_social_hosts/website/static/social_hosts.db"

@app.route("/")
def home():
    """Display information on social hosting in general."""
    return render_template('home.html')

@app.route("/home.html")
def home_html():
    """Return to the home page"""
    return render_template('home.html')

@app.route("/your_schedule.html", methods=['GET', 'POST'])
def your_schedule():
    """Find individual schedule by name."""
    if request.method == "POST":
        name = request.form.get("name").title()
        if not name:
            error = "Please enter a valid and eligible social host's name"
            return render_template('your_schedule.html', error=error)
        else:
            with sqlite3.connect(db_path) as conn:
                schedule = conn.execute(
                    "SELECT Overs, Unders, Date FROM social_hosts WHERE Overs = :name OR Unders LIKE '%' || :name || '%';",
                    {"name": name}).fetchall()
                return render_template('your_schedule.html', name=name, schedule=schedule)
    else:
        return render_template('your_schedule.html')

@app.route("/full_schedule.html", methods=['GET', 'POST'])
def full_schedule():
    """Find who is social hosting by the date they put in."""
    if request.method == "POST":
        date = request.form.get("date")
        if not date:
            error = "Please select a date"
            return render_template('full_schedule.html', error=error)
        elif date < "2025-04-06" and date > "2024-08-29":
            with sqlite3.connect(db_path) as conn:
                schedule = conn.execute(
                    "SELECT Overs, Unders FROM social_hosts WHERE Date = :date;",
                    {"date": date}
                ).fetchall()
            return render_template('full_schedule.html', date=date, schedule=schedule)
    return render_template('full_schedule.html')

if __name__ == "__main__":
    app.run(debug=True)
