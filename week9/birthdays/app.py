import os
import sys

# from cs50 import SQL
import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database

# db = SQL("sqlite:///birthdays.db")
def get_db_connection():
    conn = sqlite3.connect('birthdays.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        if name == "" or month == "" or day == "":
            return render_template("failure.html")
        
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?);",
            (name, month, day),
        )
        conn.commit()
        conn.close()

        return redirect("/")

    else:
        conn = get_db_connection()
        birthdays = conn.execute("SELECT * FROM birthdays").fetchall()
        conn.close()
        return render_template("index.html", birthdays=birthdays)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    id = request.form.get("id")
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM birthdays WHERE id = ?;",
        id,
    )
    conn.commit()
    conn.close()
    return redirect("/")
