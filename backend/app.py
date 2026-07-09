"""
This is the main application file for the Flask web application. It defines the routes and their corresponding view functions. 
The application serves two routes: the root route ('/') which renders the 'index.html' template, and the '/poista' route which renders the 'poista.html' template. 
The application runs on the default Flask development server when executed directly.
"""
from flask import Flask, render_template, request, session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_mysqldb import MySQL
import dbinfo
import bcrypt
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

app.config['MYSQL_HOST'] = dbinfo.data["HOST"]
app.config['MYSQL_USER'] = dbinfo.data["USER"]
app.config['MYSQL_PASSWORD'] = dbinfo.data["PASSWORD"]
app.config['MYSQL_DB'] = dbinfo.data["DBNIMI"]

mysql = MySQL(app)

class MyForm(FlaskForm):
    """
    a form for user login, containing fields for username and password.
    """
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Handles the login functionality of the application.
    Renders the 'login.html' template and processes the login form submission.
    """
    form = MyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            print(f"Username: {username}, Password: {password}")
            cursor = mysql.connection.cursor()    
            cursor.execute('SELECT * FROM admin WHERE username = %s', (username,))
            user = cursor.fetchall()            
            # encoding user password
            getpassword = password.encode('utf-8')
            storedpassword = user[0][2].encode('utf-8')
            # checking password
            result = bcrypt.checkpw(getpassword, storedpassword)
            if result == True:
                session['id'] = user[0][0]
                session['username'] = username
                session['logged_in'] = True
                return redirect('/home')
            else:
                return render_template('login.html', form=form)
            
    return render_template('login.html', form=form)

@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    Renders the 'home' page of the application with basic statistics.
    """
    if session.get('logged_in') is None or session.get('id') == None or session.get('username') == None:
        return redirect('/')

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM kalastaja')
    users_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM laji')
    species_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM vapa')
    rods_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM viehe')
    lures_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tarppi')
    trips_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM kala')
    fish_count = cursor.fetchone()[0]

    return render_template(
        'home.html',
        users_count=users_count,
        species_count=species_count,
        rods_count=rods_count,
        lures_count=lures_count,
        trips_count=trips_count,
        fish_count=fish_count
    )

@app.route('/poista', methods=['GET', 'POST'])
def poista():
    """
    Renders the 'poista' page of the application.
    """
    if session.get('logged_in') is None or session.get('id') == None or session.get('username') == None:
        return redirect('/')
    
    cursor = mysql.connection.cursor()    
    cursor.execute('SELECT id, email FROM kalastaja')
    users = cursor.fetchall()      

    cursor = mysql.connection.cursor()    
    cursor.execute('SELECT id, laji FROM laji')
    laji = cursor.fetchall()   

    
    cursor = mysql.connection.cursor()    
    cursor.execute('SELECT id, vapa FROM vapa')
    vapa = cursor.fetchall()      
          

    cursor = mysql.connection.cursor()    
    cursor.execute('SELECT id, viehe FROM viehe')
    viehe = cursor.fetchall()      
        
    return render_template('poista.html', users=users, users_length=len(users), laji=laji, laji_length=len(laji), vapa=vapa, vapa_length=len(vapa), viehe=viehe, viehe_length=len(viehe))

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    """
    Handles the deletion of a user from the database.
    Expects a POST request with the 'users' form field containing the ID of the user to delete.
    """
    if session.get('logged_in') is None or session.get('id') == None or session.get('username') == None:
        return redirect('/')
    
    if request.method == 'POST':
        user_id = request.form.get('users')
        s = user_id.split(',')[1]
        s = re.sub("[)']", "", s) 
        cursor = mysql.connection.cursor()
        # poistetaan käyttäjä ja siihen kuuluvat tiedot
        cursor.execute(f"SELECT id FROM kalastaja WHERE email='{s.strip()}'")
        kayttajat_id = cursor.fetchall()
        cursor.execute(f"SELECT id FROM tarppi WHERE kalastaja_id='{kayttajat_id[0][0]}'")
        tarppi_idt = cursor.fetchall()
        for c in tarppi_idt:
            cursor.execute(f"DELETE FROM kala WHERE tarppi_id='{c[0]}'")
        cursor.execute(f"DELETE FROM tarppi WHERE kalastaja_id='{kayttajat_id[0][0]}'")
        cursor.execute(f"DELETE FROM kalastaja WHERE email='{s.strip()}'")
        # tallettaa tapahtuneen tietokantaan
        mysql.connection.commit()
        print(f"User with email {s.strip()} has been deleted.")

        return redirect('/poista')
    
    return redirect('/poista')

@app.route('/delete_vapa', methods=['GET', 'POST'])
def delete_vapa():
    pass

@app.route('/delete_laji', methods=['GET', 'POST'])
def delete_laji():
    pass

@app.route('/delete_viehe', methods=['GET', 'POST'])
def delete_viehe():
    pass

@app.route('/logout')
def logout():
    """
    Logs out the current user by clearing the session and redirecting to the login page.
    """
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run()
