from flask import Flask,request,flash,make_response,redirect,abort, render_template, session, url_for
import sqlite3
from flask_bootstrap import Bootstrap
from flask_moment import moment
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField,SubmitField
from wtforms.validators import InputRequired,Length
import os
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
#app.config["secret_key"] = 'uwequwyequwe-1625361253-ajsgdvhasgd-125631'
application = app
app.secret_key = os.urandom(24)  # Generates a 24-byte random key
bootstrap = Bootstrap(app)
Moment = moment(app)




class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[InputRequired()])
    submit = SubmitField('Submit')




def init_db():
   conn  = sqlite3.connect('database.db')
   cursor = conn.cursor()
   # Create a table if it doesn't exist
   cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            published_year INTEGER
        )
    ''') 
#    cursor.execute("DROP TABLE IF EXISTS users")
#    conn.commit()

   cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
   cursor.execute('SELECT COUNT(*) FROM users')
   count = cursor.fetchone()[0] 
   if count == 0:
        dummy_users = [
            ('atoz@abc.com',generate_password_hash("qwerqwerty")),
            ('gotoz@goh.com',generate_password_hash('aqvwert'))
          
        ]
         # Always insert fresh test data
        test_users = [
        ('atoz@abc.com', generate_password_hash("qwerqwerty")),
        ('gotoz@goh.com', generate_password_hash('aqvwert'))
        ]
    
        print("Generated hashes:")  # Debug print
        for user in test_users:
            print(f"Username: {user[0]}, Hash: {user[1]}")

        cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', test_users)
        conn.commit()
    
   cursor.execute('SELECT COUNT(*) FROM books')
   count = cursor.fetchone()[0] 
   if count == 0:
        dummy_books = [
            ('The Great Gatsby', 'F. Scott Fitzgerald', 1925),
            ('To Kill a Mockingbird', 'Harper Lee', 1960),
            ('1984', 'George Orwell', 1949),
            ('Pride and Prejudice', 'Jane Austen', 1813),
            ('The Hobbit', 'J.R.R. Tolkien', 1937)
        ]
        cursor.executemany('INSERT INTO books (title, author, published_year) VALUES (?, ?, ?)', dummy_books)  
        conn.commit()

        conn.close()
   
init_db()

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    submit = SubmitField('Login')

@app.route('/login',methods=["GET","POST"])
def login():
   form = LoginForm()
   print(form.data)
   if form.validate_on_submit():
      conn = sqlite3.connect('database.db')
      cursor= conn.cursor()      
      cursor.execute('Select * FROM users WHERE username=?',(form.username.data.strip(),))
      
      
      user = cursor.fetchone()       
      print(user[2])       
      conn.close()

      if user and check_password_hash(user[2],form.password.data.strip()):
         session['user_id'] = user[0]
         session['username'] = user[1]
         flash('Login sucessful !')
         return redirect(url_for('dashboard'))
      else:
         flash('Invalid Username or Password')
   return render_template('login.html', form=form)
     

@app.route('/fetch')
def fetch():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return render_template('fetch.html', books=books)

    

@app.route('/index')
def home():
   return render_template('home.html')

@app.route('/')
def index():
  response = make_response('<h1>This document carries a cookie!</h1>')
  response.set_cookie('answer', '42')
  response.status_code = 400
  return response


@app.route('/user/<name>')
def user(name):
 user_agent= request.headers.get("user-agent")
 return '<h1>Hello, %s!</h1>' % name

@app.route("/google")
def Google():
     return redirect("https://www.google.com")   

@app.route('/private/<int:id>')
def get_user(id):    
    if id==23:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name

@app.route("/find")
def find():
   return '<h1>Hello World</h1>',510

@app.route('/hello/<name>')
def hello(name):
   return render_template('index.html',user=name)

@app.route('/derived')
def derived():
   return render_template('derived.html')

@app.route('/loops')
def loops():
   return render_template('loop.html',comments=["COMMENT1","COMMENT2","COMMENT3"])

@app.route('/form', methods=["GET","POST"])
def receiveinfo():
   #name = None
   form = NameForm()
   print(form.name.data)
   if form.validate():
     # name = form.name.data
      session['name'] = form.name.data #form.username.data
      form.name.data =''     
      flash('taking you to next page')      
      return  redirect(url_for('dashboard'))
   return render_template('form.html',form=form,name = session.get('name'))
   
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()  # Remove all session data
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))
    
        
   
   

if __name__ == '__main__':
 application.run(debug=True)



