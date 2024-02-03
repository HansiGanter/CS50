import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from functools import reduce
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    cash = db.execute("SELECT cash FROM  users WHERE id = ?;", session["user_id"])
    if len(cash) <= 0:
        return apology("user not in database", 403)
    cash = cash[0]["cash"]
    stocks = db.execute(
        "SELECT stock_symbol , sum(num_shares) AS shares FROM transactions GROUP BY stock_symbol HAVING user_id = ?;", session["user_id"])
    stocks = [{**stock, 'price': lookup(stock['stock_symbol'])['price'],
               'name': lookup(stock['stock_symbol'])['name']} for stock in stocks]
    total = reduce(lambda acc, stock: acc + stock['price'] * stock['shares'], stocks, 0) + cash

    for stock in stocks:
        stock['total'] = usd(stock['price']* stock['shares'])
        stock['price'] = usd(stock['price'])

    return render_template("index.html", stocks=stocks, cash=cash, total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol") or lookup(request.form.get("symbol")) == None:
            return apology("must provide valid symbol", 400)

        # Ensure shares was submitted
        if not request.form.get("shares"):
            return apology("must provide shares", 400)

        elif not request.form.get("shares").isdigit():
            return apology("num of shares must be integer", 400)

        price = lookup(request.form.get("symbol"))["price"]
        cash = float(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash'])

        if (price * float(request.form.get("shares"))) > cash:
            return apology("not enough cash", 400)

        db.execute("INSERT INTO transactions (created_at, stock_symbol, num_shares, price_share, user_id) VALUES (?, ?, ?, ?,?);", datetime.now(
        ).strftime('%Y-%m-%d %H:%M:%S'), request.form.get("symbol").upper(), request.form.get("shares"), price, session["user_id"])
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?;", price * float(request.form.get("shares")), session["user_id"])

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT CASE WHEN num_shares > 0 THEN 'buy' WHEN num_shares < 0 THEN 'sell' END AS transaction_type, num_shares * price_share AS total, * FROM transactions WHERE user_id = ?;", session["user_id"])

    for transaction in transactions:
        transaction['price_share'] = usd(transaction['price_share'])
        transaction['total'] = usd(transaction['total'])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        stock = lookup(request.form.get("symbol"))

        if stock is None:
            return apology("must provide valid stock symbol", 400)

        stock["price"]=usd(stock["price"])
        return render_template("quoted.html", stock=stock)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match", 400)

        pattern = re.compile(r'^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$')
        if not pattern.match(request.form.get("password")):
            return apology("Password must contain at least one number and one special character, and at least 8 or more characters")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username doesn't exist
        if len(rows) > 0 and rows[0]['username'] == request.form.get("username"):
            return apology("username already exists", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (?,?);", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        # Redirect user to home page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        stocks = db.execute(
            "SELECT stock_symbol, sum(num_shares) AS shares FROM transactions GROUP BY stock_symbol HAVING user_id = ?;", session["user_id"])

        if not any(stock['stock_symbol'].upper() == request.form.get("symbol").upper() for stock in stocks):
            return apology(f"You don't have any {request.form.get('symbol')} stocks", 400)

        if next((item for item in stocks if item['stock_symbol'].upper() == request.form.get("symbol").upper()), None)['shares'] < int(request.form.get("shares")):
            return apology(f"You have less then {request.form.get('shares')} {request.form.get('symbol')} stocks", 400)

        price = float(lookup(request.form.get('symbol'))['price'])

        db.execute("INSERT INTO transactions (created_at, stock_symbol, num_shares, price_share, user_id) VALUES (?, ?, ?, ?,?);", datetime.now(
        ).strftime('%Y-%m-%d %H:%M:%S'), request.form.get("symbol"), int(request.form.get("shares"))*-1, price, session["user_id"])
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?;", price * float(request.form.get("shares")), session["user_id"])

        return redirect('/')

    else:
        stocks = db.execute(
            "SELECT stock_symbol, sum(num_shares) AS shares FROM transactions GROUP BY stock_symbol HAVING user_id = ?;", session["user_id"])
        return render_template("sell.html", stocks=stocks)


@app.route("/changepwd", methods=["GET", "POST"])
@login_required
def changepwd():
    """Change Password"""

    if request.method == "POST":
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide old password", 403)

        elif not request.form.get("newpassword"):
            return apology("must provide new password", 403)

        elif not request.form.get("confirmation"):
            return apology("must confirm new password", 403)

        elif request.form.get("newpassword") != request.form.get("confirmation"):
            return apology("Passwords don't match", 403)

        pattern = re.compile(r'^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$')
        if not pattern.match(request.form.get("newpassword")):
            return apology("Password must contain at least one number and one special character, and at least 8 or more characters")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("wrong password", 403)

        db.execute("UPDATE users SET hash = ? WHERE id = ?;", generate_password_hash(
            request.form.get("newpassword")), session["user_id"])

        return redirect("/")
    else:
        return render_template("changepwd.html")


@app.route("/addcash", methods=["POST"])
@login_required
def addcash():
    """Add Cash to Account"""
    if not request.form.get("cash") or not request.form.get("cash").isnumeric():
        return apology("must provide cash amount", 403)

    db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", float(request.form.get("cash")), session["user_id"])
    return redirect("/")
