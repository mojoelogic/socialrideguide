from flask import Flask, render_template, send_from_directory, request, redirect
import csv

app = Flask(__name__)


# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

@app.route('/')
def home():
    return render_template('index.html')


def write_to_ideas(data):
    with open('ideas_db.csv', newline='', mode='a') as database:
        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(
            database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, )
        csv_writer.writerow([name, email, subject, message])


def write_to_email_list(data):
    with open('email_list_db.csv', newline='', mode='a') as database:
        name = data["name"]
        email = data["email"]
        csv_writer = csv.writer(
            database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, )
        csv_writer.writerow([name, email])


@app.route('/signup_submit', methods=['POST', 'GET'])
def signup_submit():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_email_list(data)
            return redirect('/#thank_you')
        except:
            return "Sorry the wheels came off. It didn't save."
    else:
        return "Looks like we had a mechanical. Would you mind backing up and trying that again friend?"


@app.route('/ideas_submit', methods=['POST', 'GET'])
def ideas_submit():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_ideas(data)
            return redirect('/#thank_you')
        except:
            return "Sorry the wheels came off. It didn't save."
    else:
        return "Looks like we had a mechanical. Would you mind backing up and trying that again friend?"
