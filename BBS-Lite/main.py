from flask import Flask, redirect, url_for, render_template,request, session, flash
from flask_bcrypt import Bcrypt #User authentication 
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os




app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = "help!" # Please change this key to any key you want
app.permanent_session_lifetime = timedelta(minutes=10)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # Data base file and name
app.config['SQLALCHEMY_TRACH_MODIFICATIONS'] = True


db = SQLAlchemy(app)

class utility(db.Model):# Utility function
    _id = db.Column("id",db.Integer, primary_key=True)
    name = db.Column("name", db.String(200),nullable=False)
    param = db.Column(db.Integer)

    def __init__(self,name,param):
        self.name = name
        self.param = param


class users(db.Model): # User data base
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(200),nullable=False)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    sex = db.Column(db.String(8))

    def __init__(self,name,email,password,sex=None):
        self.name = name
        self.email = email
        self.password = password

class entries(db.Model): # Posts
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(200))
    content = db.Column(db.String(3000))

    def __init__(self,_id,title,content,author="Author not found"):
        self._id=_id
        self.title = title
        self.content = content
        self.author = author
        

class replies(db.Model): #replies
    _id = db.Column("id", db.Integer, primary_key=True)
    adressing_id = db.Column(db.String(100))  # id of the post replying to
    name  = db.Column(db.String(200))
    reply = db.Column(db.String(1000))

    def __init__(self,name,adressing_id,reply):
        self.name = name
        self.adressing_id = adressing_id
        self.reply = reply



@app.route("/admin") # access this page manually
def admin_page():

    if "user" in session:
        pass
    else:
        return redirect(url_for("home"))

    if session["user"] == "admin":
        return render_template("admin.html", 
            name="admin",values=users.query.all(),
            entries=entries.query.all(),
            found_replies=replies.query.all(),
            last_post_id=utility.query.filter_by(name="Last_entry_id").first().param,
            last_reply_id=utility.query.filter_by(name="Last_reply_id").first().param
            )
    else:
        return redirect(url_for("home"))


@app.route("/", methods = ["GET","POST"]) # index page
def home():
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            utility.query.filter_by(name="Last_entry_id").first().param += 1
            last_post_id = utility.query.filter_by(name="Last_entry_id").first().param
            db.session.add(entries(last_post_id, request.form["submit_title"],request.form["submit_content"],session["user"]))
            db.session.commit()
            return redirect(url_for("home"))
    else:
        user = "Default_user"
    return render_template("index.html",name=user,values=entries.query.all())


@app.route("/posts/<post_id>", methods = ["GET","POST"]) # post page
def posts(post_id):
    found_post=entries.query.filter_by(_id=post_id).first()
    if found_post:
        post_id=found_post._id
        post_title=found_post.title
        post_content=found_post
        if request.method == "POST":
            if "user" in session:

                db.session.add(replies(session["user"], post_id, request.form["reply_content"]))
                utility.query.filter_by(name="Last_reply_id").first().param += 1
        db.session.commit()
        found_replies=replies.query.filter_by(adressing_id=post_id).all()
        return render_template("posts.html", found_post=found_post,replies=found_replies[::-1])

    else:
        return "<h1> No relevant page found!!!</h1>"
    

@app.route("/login", methods = ["GET","POST"]) #login page
def login_page():
    error = ""
    try:
        if request.method == "POST":
            session.permanent = True
            user_name = request.form["user_name"]
            password = request.form["password"]
            found_user = users.query.filter_by(name=user_name).first()
            if found_user: 
                if bcrypt.check_password_hash(found_user.password, password):#check if hash is correct
                    session["user"] = found_user.name
                    session["email"] = found_user.email
                    flash("You are logged in", "info")
                    return redirect(url_for("user"))
                else:
                    raise Exception("Invalid Credentials")
            else:
                raise Exception("No User")
        else:
            return render_template("login.html")

    except Exception as e:
        error=e
        return render_template("login.html", error = error)



@app.route("/register", methods = ["GET","POST"]) #registering page
def register():
    email = None
    if request.method == "POST":
        session.permanent = True
        user_name = request.form["user_name"]
        email = request.form["email"]
        pas=request.form["password"]
        password = bcrypt.generate_password_hash(pas)
        found_user = users.query.filter_by(name=user_name).first()
        if found_user:
            flash("Account has been registered!!!","error_registration")
            return render_template("register.html")
        
        else:
            session["user"] = user_name
            session["email"] = email
            db.session.add(users(user_name,email,password))
            db.session.commit()
            flash(f"Account Created, your email is {email}", "info")
            return redirect(url_for("user"))

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email",None)
    flash("You are logged out", "info")
    return redirect(url_for("home"))



@app.route("/user")
def user():
    if "user" in session:
        print(session)
        user = session["user"]
        email = session["email"]
        return render_template("user.html",name=user,email=email)
    else:
        print("user not in session")
        return redirect(url_for("login_page"))




if __name__ == "__main__":
    db.create_all()

    db.session.add(utility("Last_entry_id",20))
    db.session.add(utility("Last_reply_id",20))
    db.session.commit()

    app.run(debug=True,host='0.0.0.0', port=8080)
