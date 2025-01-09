from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/", methods=["GET", "POST"])
def login():
    print("login")
    if request.method == "POST":
        email = request.form["e-mail"]
        password = request.form["password"]
        return validate(email, password)
    return render_template("login.html")


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        email = request.form["e-mail"]
        password = request.form["password"]
        conn = sql.connect("users.db")
        cur = conn.cursor()
        cur.execute(f"""SELECT 1
                        FROM users
                        WHERE email LIKE '{email}'""")
        user = cur.fetchone()
        if user==None:
            cur.execute(f"""INSERT INTO users (email, password)
                            VALUES ('{email}', '{password}')""")
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        else:
            # utente già esistente
            pass
    return render_template("create_account.html")


@app.route("/logout")
def logout():
    return redirect(url_for("login"))

def validate(username, password):
    conn = sql.connect("users.db")
    cur = conn.cursor()
    cur.execute(f"""SELECT users.password
                    FROM users
                    WHERE email LIKE '{username}'""")
    pswd = cur.fetchone()
    print(pswd)
    if pswd[0] == password:
        return redirect(url_for("home"))
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4444)
