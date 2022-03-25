from flask import Flask, render_template, request, redirect, flash, send_from_directory, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'verysecretkey'
client = MongoClient('localhost', 27017)
db = client.practice1


@app.route('/')  # starting page
def index():
    return render_template('index.html')

# message flashing
# https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/


@app.route('/signup', methods=['GET', 'POST'])  # signup page
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    else:
        username = request.form.get('username')
        password = request.form.get('password')

        if db.users.count_documents({'username': username}) != 0:
            flash('Username already exists! Try another one!')
            return redirect('/signup')

        else:
            db.users.insert_one({
                'username': username,
                'password': password
            })
            flash('Signed up! Hello ' + username)
            return redirect('/auth')


@app.route('/auth', methods=['GET', 'POST'])  # auth
def auth():
    if request.method == 'GET':
        return render_template('auth.html')

    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.users.find_one({'username': username})

        if (user and user['password'] == password):
            flash('Hello ' + username)
            return render_template('secret.html')

        else:
            flash('Username or password in not correct! Try again!')
            return render_template('auth.html')


# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
allowed_extensions = {'jpg', 'png', 'jpeg'}
# allowed extensions for upload


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    else:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if not file or file.name == '':
            flash('No selected file')
            return redirect(request.url)

        if file and not allowed_file(file.filename):
            flash('Invalid file extension')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file.save(os.path.join('upload', filename))
        return redirect(url_for('uploaded', filename=filename))


@app.route('/uploaded/<path:filename>')
def uploaded(filename):
    return send_from_directory('upload', filename)


@app.route('/notebook', methods=['GET', 'POST'])
def notebook():
    if request.method == 'GET':
        number_of_notes = request.args.get(
            'number_of_notes')  # ?number_of_notes=x min=1

        if number_of_notes and int(number_of_notes) > 0:
            notes = list(db.notes.find({}).limit(int(number_of_notes)))

        else:
            notes = list(db.notes.find({}))

        return render_template('notebook.html', notes=notes, number=len(notes))

    else:
        note_title = request.form.get('note_title')
        note_content = request.form.get('note_content')
        db.notes.insert_one({
            'note_title': note_title,
            'note_content': note_content
        })
        flash("Note added!")

        notes = list(db.notes.find({}))
        return render_template('notebook.html', notes=notes, number=len(notes))


@app.route('/notebook/delete', methods=['POST'])
def delete_notes():
    db.notes.drop()
    return redirect('/notebook')


'''
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

 '''

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
