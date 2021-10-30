# conda activate PIC 16B
# export FLASK_ENV=development
# flask run


from flask import Flask, g, render_template, request, current_app
import sqlite3

app = Flask(__name__)

#shows the base.html for navigation.
@app.route('/')
def main():
    return render_template('base.html')

#submit is accessed, if message received, shows thanks, otherwise shows error.
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            insert_message(request)
            return render_template('submit.html', thanks = True)
        except:
            return render_template('submit.html', error = True)

@app.route('/view/')
def view():
	random_message = random_messages(5)
    
	return render_template('view.html', messages = random_message)


def get_message_db():
        """
        Corresponding init.sql file:

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            handle TEXT UNIQUE NOT NULL,
            message TEXT NOT NULL
        );
        """

	if 'message_db' not in g:
		g.message_db = sqlite3.connect('message_db.sqlite')

	with current_app.open_resource('init.sql') as f:
		g.message_db.executescript(f.read().decode('utf8'))

	return g.message_db

def insert_message(request):
    #connect to the database
	db = get_message_db()
    #retreive name and message
    
    name = request.form['name']
    message = request.form['message']
        
    #save name and message into the database.
	db.execute(
		'INSERT INTO messages (handle, message) VALUES (?, ?)',
		(name, message)
		)
    #ensure the row insertion is saved.
	db.commit()

    #make sure ID is unique, and close the connection.
	g.pop('message_db', None)
	db.close()


def random_messages(n):
    #connect to the database
	db = get_message_db()

	random_message = db.execute(
		f'SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT {n}'
		).fetchall()
	return random_message
