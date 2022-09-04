import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    if not session["user_id"] > 0:
        return render_template("login.html")
    elif db.execute("SELECT * FROM purchases WHERE user_id == :id", id=session["user_id"]) == None:
        return render_template("quote.html")

    else:
        results = db.execute(
            "SELECT name,symbol,SUM(number) AS shares,price FROM purchases WHERE user_id == :id GROUP BY symbol", id=session["user_id"])
        cash = db.execute("SELECT cash FROM users WHERE id == :id", id=session["user_id"])

        tableInfo = []
        grandTotal = cash[0]["cash"]
        for result in results:
            symbol = results[0]["symbol"]
            shares = int(results[0]["shares"])
            name = results[0]["name"]
            stock = lookup(symbol)
            price = float(stock["price"])
            tableInfo.append(result)
            grandTotal += shares*price

        return render_template("index.html", stocks=tableInfo, grandTotal=usd(grandTotal), cash=usd(cash[0]["cash"]))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        result = lookup(request.form.get("symbol"))

        if result == None:
            return apology("symbol not found", 400)
        elif not request.form.get("shares").isdigit():
            return apology("invalid number of shares", 400)
        elif (int(request.form.get("shares")) <= 0):
            return apology("invalid number of shares", 400)

        user_id = session["user_id"]
        cost = float(request.form.get("shares"))*float(result["price"])
        row = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        cash = float(row[0]["cash"])
        if cost > cash:
            return apology("not enough money", 400)

        name = result["name"]
        symbol = result["symbol"]
        price = result["price"]

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash-cost, user_id)
        db.execute("INSERT INTO purchases (user_id, symbol, number, name, price, type, total) VALUES (?,?,?,?,?,?,?)",
                   user_id, symbol, request.form.get("shares"), name, price, "buy", cost)
        return render_template("bought.html", result=result, cost=cost, number=request.form.get("shares"), cash=cash-cost)

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    results = db.execute("SELECT * FROM purchases WHERE user_id == :id", id=session["user_id"])
    tableInfo = []
    for result in results:
        symbol = results[0]["symbol"]
        number = int(results[0]["number"])
        name = results[0]["name"]
        type = results[0]["type"]
        price = results[0]["price"]
        total = float(results[0]["total"])
        time = results[0]["time"]
        tableInfo.append(result)

    return render_template("history.html", stocks=tableInfo)


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
    if request.method == "POST":
        result = lookup(request.form.get("symbol"))

        if result == None:
            return apology("symbol not found", 400)

        return render_template("quoted.html", result=result)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username does not already exist
        if len(rows) != 0:
            return apology("username already exists", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Redirect user to home page
        db.execute("INSERT INTO users (username, hash) VALUES ((?), (?))", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    results = db.execute("SELECT symbol FROM purchases WHERE user_id == :id GROUP BY symbol", id=session["user_id"])
    symbols = []
    for i in range(len(results)):
        symbols.append(results[i]['symbol'].upper())

    if request.method == "POST":

        if not request.form.get("symbol") in symbols:
            return apology("symbol not found in purchases", 400)
        elif int(request.form.get("shares")) < 1:
            return apology("not enough shares", 400)
        row = db.execute("SELECT SUM(number) AS total FROM purchases WHERE symbol == :symbol AND user_id == :id GROUP BY symbol",
                         symbol=request.form.get("symbol"), id=session["user_id"])
        if int(request.form.get("shares")) > row[0]['total']:
            return apology("bruh...you don't own that many shares", 400)

        user_id = session["user_id"]
        result = lookup(request.form.get("symbol"))
        price = float(request.form.get("shares"))*float(result["price"])
        row = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        cash = float(row[0]["cash"])
        number = (-1)*int(request.form.get("shares"))
        name = result["name"]
        symbol = result["symbol"]
        p = result["price"]

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash+price, user_id)
        db.execute("INSERT INTO purchases (user_id, symbol, number, name, price, type, total) VALUES (?,?,?,?,?,?,?)",
                   user_id, symbol, number, name, p, "sell", price)
        return render_template("bought.html", result=result, cost=price, number=request.form.get("shares"), cash=cash+price)

    else:
        return render_template("sell.html", symbols=symbols)

@app.route("/money")
@login_required
def money():
    """More money"""
    db.execute("UPDATE users SET cash = ? WHERE id = ? ", "10000", session["user_id"])
    return redirect("/")
