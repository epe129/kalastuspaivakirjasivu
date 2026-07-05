"""
This is the main application file for the Flask web application. It defines the routes and their corresponding view functions. 
The application serves two routes: the root route ('/') which renders the 'index.html' template, and the '/poista' route which renders the 'poista.html' template. 
The application runs on the default Flask development server when executed directly.
"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    """
    Renders the main page of the application.
    """
    return render_template('index.html')

@app.route('/poista')
def poista():
    """
    Renders the 'poista' page of the application.
    """
    return render_template('poista.html')

if __name__ == '__main__':
    app.run()
