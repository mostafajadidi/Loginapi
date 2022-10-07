from ast import Break
from flask import session, redirect, url_for, request,  render_template
from flask  import Flask
import psycopg2
import hashlib

app = Flask(__name__)
app.secret_key = 'any random string'

conn = psycopg2.connect(
    database="Daraya1", user='postgres', password='Daraya123', host='localhost', port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()


@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('Login1.html')

@app.route('/', methods = ['GET', 'POST'])
def index():
    cursor.execute('''SELECT * from useraccount''')
    result = cursor.fetchall()
    if 'Signup' in session and request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = (hashlib.sha256(password.encode())).hexdigest()
        cursor.execute("INSERT INTO useraccount( username , password) VALUES (%s,%s)",(username,password))
        session.pop('Signup', None)
        return redirect(url_for('login'))


    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        if 'username' in session:
            username = session['username']
            password = session['password']
            password = (hashlib.sha256(password.encode())).hexdigest()
            i=0
            for d in result:
                if (d[0]==username and d[1]==password):
                    return 'Logged in as ' + username + '<br>' + \
                    "<b><a href = '/logout'>click here to log out</a></b>"
                else:
                    i = i+1
        if i==len(result):
            return 'Incorrect Pass' '<br>' + \
                 "<b><a href = '/Signup'>click here to Signup</a></b>"
        
        return redirect(url_for('login'))

    return "You are not logged in <br><a href = '/login'></b>" + \
      "click here to log in</b></a>"

@app.route('/Signup', methods = ['GET', 'POST'])
def Signup():
    session['Signup'] = 'Signup'
    return render_template('Signup.html')



@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(debug = True)