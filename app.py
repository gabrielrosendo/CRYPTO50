import requests
import os

from datetime import date
from tempfile import mkdtemp
from cs50 import SQL
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

from apy import lookup, usd, check

app = Flask(__name__)

#Configure Session
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
session(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


db = SQL("sqlite:///crypto.db")

if __name__ == "__main__":
    app.run()

@app.route("/register", methods=["GET", "POST"])
def register():
     ##Register user
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("register.html", error="must provide username")
        if not request.form.get("password"):
            return render_template("register.html", error="must provide password")
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html", error="passwords are different")
        # if all info was provided, create account
        username=request.form.get("username")
        password=request.form.get("password")
        # check if username is taken
        rows=db.execute("SELECT * from users WHERE username = ?", username)
        if len(rows)>0:
            return render_template("register.html", error="username is already taken")
        hash=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        return render_template("login.html")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", error="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", error="must provide password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", error="invalid username and/or password")

        #Remember who logged in
        session["user_id"]=rows[0]["id"]

        #Redirect to homepage
        return redirect("/")

    if request.method == "GET":
        return render_template("login.html")

@app.route("/")
@login_required
def index():
    crypto_owned=db.execute("SELECT symbol, price, quantity, total FROM portfolio WHERE id=:id", id= session["user_id"])
    for symbol in crypto_owned:
        quote=symbol['symbol']
        now_price=lookup(quote)['price']
        name=lookup(quote)['name']
        change_24=lookup(quote)['change_24']
        quantity=symbol['quantity']
        total_worth=quantity*now_price
        db.execute("UPDATE portfolio SET price_now=:price_new, total_now=:total_new, change_24= :change_24h, name=:name WHERE id=:id AND symbol=:symbol",
        id=session["user_id"], symbol=quote, price_new=usd(now_price), total_new=usd(total_worth), change_24h=round(change_24,2), name=name)
    data=db.execute("SELECT id, symbol, name, price, total, quantity, price_now, total_now, change_24 FROM portfolio WHERE id=:id", id=session["user_id"])
    titles=check()
    for title in titles:
        print(title)
    
    today=date.today()    
    return render_template("index.html", data=data, today=today, titles=titles)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        cash=db.execute("SELECT cash FROM users WHERE id=:id",  id = session["user_id"])
        return render_template("buy.html", cash=usd(cash[0]['cash']))

    if request.method == "POST":
        cash=db.execute("SELECT cash FROM users WHERE id=:id",  id = session["user_id"])

        if not request.form.get("symbol"):
            return render_template("buy.html", error="invalid symbol", cash=usd(cash[0]['cash']))
        if not request.form.get("quantity"):
            return render_template("buy.html", error="invalid number of shares", cash=usd(cash[0]['cash']))
        symbol=(request.form.get("symbol")).upper()
        lookedup=lookup(symbol)
        if not lookedup:
            return render_template("buy.html", error="invalid crypto symbol", cash=usd(cash[0]['cash']))

        info=lookup(symbol)
        quantity=float(request.form.get("quantity"))
        price=round(float(info.get('price')),2)
        total=price*quantity
        rounded_total=round(total, 2)


        old_cashlist=db.execute("SELECT cash FROM users WHERE id=:id",  id = session["user_id"])
        old_cash=old_cashlist[0]['cash']

        new_cash=old_cash-total
        if new_cash<0:
            return render_template("buy.html", error="you can't afford this transaction", cash=usd(cash[0]['cash']))
        else:
            db.execute("INSERT INTO portfolio(id, symbol, price, quantity, total) VALUES (:id, :symbol, :price, :quantity, :total)", id= session["user_id"], symbol=symbol, price=price, quantity=quantity, total=rounded_total)
            db.execute("UPDATE users SET cash =:cash WHERE id=:id", cash=new_cash, id= session["user_id"])
        return redirect(url_for("index"))



@app.route("/crypto")
@login_required
def crypto():
    return render_template("crypto.html")
    
@app.route("/logout")
def logout():
    session.clear()
    
    return redirect("/")    
    
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        quote = request.args.get('q')
        price = lookup(quote)['price']
        dados=db.execute("SELECT quantity FROM portfolio WHERE id=:id AND symbol=:symbol", id= session["user_id"], symbol=quote)
        own=(dados[0]['quantity'])
        return render_template("sell.html", quote=quote, price=round(price,2), own=own)
        
    if request.method == "POST":
        quantity=float(request.form.get("quantity"))
        symbol=request.form.get("symbol").upper()
        price=lookup(symbol)['price']
        
        num=db.execute("SELECT quantity FROM portfolio WHERE id = :id AND symbol=:quote", id = session["user_id"], quote=symbol)
        if not num:
             return render_template("sell.html", error="invalid symbol")
        number=float(num[0]['quantity'])
        if quantity>number:
            return render_template("sell.html", error="you do not have enough to make this transaction")
        
        else:
            db.execute("UPDATE portfolio SET quantity=:shar WHERE id=:id AND symbol=:quote", shar=round(number-quantity,2), id=session["user_id"], quote=symbol)
            if quantity==number:
                db.execute("DELETE FROM portfolio WHERE symbol=:stock AND id=:id", stock=symbol.upper(), id = session["user_id"])
            old_cashlist=db.execute("SELECT cash FROM users WHERE id=:id",  id = session["user_id"])
            old_cash=old_cashlist[0]['cash']
            total_price=price*quantity
            new_cash=old_cash+total_price
            db.execute("UPDATE users SET cash=:new_cash WHERE id=:id", new_cash=new_cash, id=session["user_id"])
            return redirect(url_for("index"))

