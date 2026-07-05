"""
This is the main application file for the Flask web application. It defines the routes and their corresponding view functions. 
The application serves two routes: the root route ('/') which renders the 'index.html' template, and the '/poista' route which renders the 'poista.html' template. 
The application runs on the default Flask development server when executed directly.
"""
from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_mysqldb import MySQL
import dbinfo


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

app.config['MYSQL_HOST'] = dbinfo.data["HOST"]
app.config['MYSQL_USER'] = dbinfo.data["USER"]
app.config['MYSQL_PASSWORD'] = dbinfo.data["PASSWORD"]
app.config['MYSQL_DB'] = dbinfo.data["DBNIMI"]

mysql = MySQL(app)

cursor = mysql.connection.cursor()

class MyForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def login():
    """
    """
    form = MyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            
            cursor.execute('SELECT * FROM WHERE username = %s', (username))
            
            user = cursor.fetchone()


    return render_template('login.html', form=form)

@app.route('/poista', methods=['GET', 'POST'])
def poista():
    """
    Renders the 'poista' page of the application.
    """
    return render_template('poista.html')

if __name__ == '__main__':
    app.run()
