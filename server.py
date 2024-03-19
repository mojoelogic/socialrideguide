from flask import Flask, render_template, send_from_directory, request, redirect, make_response
import csv
import jinja2
import pdfkit

app = Flask(__name__)


# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

@app.route('/')
def home():
    return render_template('index.html')


def night_ride(ride):
    if ride == "Y":
        return True
    else:
        return False


def corking(cork):
    if cork == "Y":
        return True
    else:
        return False


@app.route('/ride_talk', methods=['POST', 'GET'])
def ride_talk():
    if request.method == 'POST':
        leader_name = request.form['leader_name']
        event_name = request.form['event_name']
        breakpoint = request.form['breakpoint']
        sweeper_name = request.form['sweeper_name']
        corker_name = request.form['corker_name']
        endpoint = request.form['endpoint']
        colead = request.form['colead']
        night_ride_clean = night_ride(request.form['night_ride'])
        corking_clean = corking(request.form['corking'])

    rendered = render_template('ride_talk_pdf.html', leader_name=leader_name, event_name=event_name,
                               breakpoint=breakpoint, sweeper_name=sweeper_name,
                               corker_name=corker_name, endpoint=endpoint,
                               colead=colead,
                               night_ride=night_ride_clean, corking=corking_clean)

    # pdf = pdfkit.from_string(rendered, False)

    # response = make_response(pdf)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'attachment; filename=preride_speech.pdf'
    return rendered


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
