import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
import datetime


# Configure application
app = Flask(__name__)

# date variabel to track date stock was bought
x = datetime.datetime.now()
date_bought = x.strftime("%x")

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
    # get dictionary of stocks owned by current user
    user_id = session["user_id"]
    user_dict = db.execute("SELECT username, cash FROM users WHERE users.id = ?", user_id)

    # get list of dictionaries of stocks bought by the user
    transactions_dict = db.execute("SELECT stock_bought, shares_owned FROM transactions WHERE transactions.user_id = ?", user_id)

    # store data in variables to pass into render template
    username = user_dict[0]["username"]
    cash = user_dict[0]["cash"]
    grand_total = cash

    # loop through list of dict objects
    for transaction in transactions_dict:
        # create variables to add to dict objects to render in html file
        price = lookup(transaction["stock_bought"])["price"]
        value_of_holdings = price * transaction["shares_owned"]
        transaction.update({'price': price, 'value_of_holdings': value_of_holdings})
        grand_total += value_of_holdings

    return render_template("index.html", cash=cash, stocks=transactions_dict, grand_total=grand_total, username=username)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Please enter a valid stock symbol", 400)

        if not request.form.get("shares"):
            return apology("Please specify the number of shares you would like to purchase", 400)

        if not request.form.get("shares").isdigit():
            return apology("You cannot purchase partial shares.")

        if int(request.form.get("shares")) < 1:
            return apology("Please enter a number greater than 0", 400)

        # find what user is using the app
        user_id = session["user_id"]

        # stock the user wishes the buy
        stock_to_buy = request.form.get("symbol")

        # the amount of shares the user wishes to buy
        quantity = request.form.get("shares")

        # contact the api
        look = lookup(stock_to_buy)

        if not look:
            return apology("Invalid stock symbol")

        # store the price to deduct in variable
        price = float(look["price"]) * float(quantity)

        # query the database for the amount of cash
        user = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = float(user[0]["cash"])

        # check if user has enough money to buy the stock
        if user_cash < price:
            return apology("Insufficient funds")

        # check if user has stock already if so update table and deduct cash
        user_stocks_db = db.execute("SELECT * FROM transactions WHERE user_id = ? AND stock_bought = ?", user_id, stock_to_buy)
        new_cash_total = user_cash - price

        if len(user_stocks_db) == 1:
            shares_quantity = user_stocks_db[0]["shares_owned"]
            new_quantity = shares_quantity + 1
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_total, user_id)
            db.execute("UPDATE transactions SET shares_owned = ? WHERE user_id = ? AND stock_bought = ?", new_quantity, user_id, stock_to_buy)
        else:
            # if user doesnt have stock update table with user_id, stock_bought, quantity and date
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_total, user_id)
            db.execute("INSERT INTO transactions (stock_bought, date, user_id, shares_owned) VALUES(?, ?, ?, ?)",
                        stock_to_buy, date_bought, user_id, quantity)

        db.execute("INSERT INTO history (type, date, number_of_shares, history_id, stock_symbol, price) VALUES (?, ?, ?, ?, ?, ?)",
                    "BUY", date_bought, quantity, session["user_id"], look["symbol"], look["price"])

        return redirect("/")

    else:

        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM history WHERE history_id = ? ORDER BY date", session["user_id"])
    print(history)
    return render_template("history.html", history=history)


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

        # Store the dictionary returned from the search
        look = lookup(request.form.get("symbol"))

        # If the symbol searched is invalid, return apology
        if look == None:
            return apology("invalid symbol", 400)

        # If the symbol exists, return the search
        else:
            return render_template("quoted.html", name=look["name"], symbol=look["symbol"], price=usd(look["price"]))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 400)

        if not request.form.get("password") or request.form.get("password") != request.form.get("confirmation"):
            return apology("missing password/passwords did not match", 400)

        username = request.form.get("username")
        password = request.form.get("password")
        hashed = generate_password_hash(password)

        if db.execute("SELECT username FROM users WHERE username = ?", username):
            return apology("username already in use, please try again", 400)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashed)

        return redirect("/login")

    else:
        return render_template('registration.html')


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    stocks = db.execute("SELECT * FROM transactions WHERE transactions.user_id = ?", user_id)

    if request.method == "POST":

        # stock symbol
        stock_to_sell = request.form.get("symbol")

        # number of shares to sell
        quantity = request.form.get("shares")

        if not quantity:
            return apology("Quantity not selected")

        if stock_to_sell == "Select a stock to sell":
            return apology("Please enter a valid stock option")

        if lookup(stock_to_sell) == None:
            return apology("Invalid symbol")

        if int(quantity) < 1:
            return apology("Please enter a value greater than 0")

        # price to be added back to cash balance
        stock_price = lookup(stock_to_sell)["price"]
        stock_symbol = lookup(stock_to_sell)["symbol"]

        transactions_dict = db.execute("SELECT * FROM transactions WHERE transactions.user_id = ? AND stock_bought = ?", session["user_id"], stock_to_sell)
        user_dict = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        amount_sold_for = stock_price * int(quantity)
        shares_owned = transactions_dict[0]["shares_owned"]
        cash = user_dict[0]["cash"]
        new_cash_balance = cash + amount_sold_for

        if int(shares_owned) < int(quantity):
            return apology("You do not own enough shares")

        if shares_owned == 1:
            # remove from transactions data base
            # add price of stock back to cash column in users
            # insert new column into history with type = SELL
            db.execute("DELETE FROM transactions WHERE user_id = ? AND stock_bought = ?", session["user_id"], stock_to_sell)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_balance, session["user_id"])

        if shares_owned > 1:
            # update shares owned
            # add price of stock back to cash column in users
            # insert new column into history with type = SELL
            new_shares = shares_owned - 1
            db.execute("UPDATE transactions SET shares_owned = ? WHERE user_id = ? AND stock_bought = ?", new_shares, session["user_id"], stock_to_sell)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_balance, session["user_id"])

        db.execute("INSERT INTO history (type, date, number_of_shares, history_id, stock_symbol, price) VALUES (?, ?, ?, ?, ?, ?)", "SELL", date_bought, quantity, session["user_id"], stock_symbol, stock_price)

        return render_template("sold.html", cash=new_cash_balance, amount=amount_sold_for)


    return render_template("sell.html", stocks=stocks)