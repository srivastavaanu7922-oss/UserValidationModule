from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    name TEXT,
    email TEXT,
    phone TEXT
)
""")

conn.commit()
cursor.execute("INSERT INTO users VALUES (?, ?, ?)", ("Anuradha", "anuradha@gmail.com", "9876543210"))
cursor.execute("INSERT INTO users VALUES (?, ?, ?)", ("Khushi", "khushi@gmail.com", "9876501234"))

conn.commit()

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        print(request.form)
        fullname = request.form.get("fullname")
        email = request.form.get("email")

        if "@" not in email or "." not in email:
            print({"valid": False, "message": "Invalid email format"})
            return render_template("index.html")
            
        phone = request.form.get("phone")

        if not phone.isdigit() or len(phone) != 10:
            print({"valid": False, "message": "Phone number must be 10 digits"})
            return render_template("index.html")

        print("Name:", fullname)
        print("Email:", email)
        print("Phone:", phone)
        
        cursor.execute(
            "SELECT * FROM users WHERE name=? AND email=? AND phone=?",
            (fullname, email, phone)
        )

        user = cursor.fetchone()

        if user:
            return render_template("index.html", result="✅ User Found")
        else:
            return render_template("index.html", result="❌ Invalid user details")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)