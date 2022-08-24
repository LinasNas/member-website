from flask import Flask, render_template, redirect, url_for
import json
from forms import CourseForm, ConfirmSig
from random_string import get_random_string

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

#MAIL
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
mail = Mail(app)

#UPLOAD BUTTON
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'edsig'}
#Max allowed size: 1MB
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1000

@app.route('/')
#append the courses_list with new info
def index():
    return render_template('index.html')

@app.route('/register/', methods=('GET', 'POST'))
def register():
    form = CourseForm()

    if form.validate_on_submit():
        profile = {
            'Name': form.name.data,
            'Affiliation': form.affiliation.data,
            'Email': form.email.data,
            'Location': form.location.data,
            'Public_key': form.public_key.data
            }

        with open("profiles/" + profile['Public_key'], 'w') as file:
            json.dump(profile, file)
        

        #email
        recipient = profile['Email']
        msg = Message('Confirm your Mainsail member registration', recipients=[recipient])
        #msg.body = ('this is body!')
        # msg.html = ('<h1>Twilio SendGrid Test Email</h1>'
        #             '<p>Congratulations! You have sent a test email with '
        #             '<b>Twilio SendGrid</b>!</p>')
        msg.html = ('<p>To confirm your registration, sign the following string with your private key:</p>'
        '<p><b> abcdef </b></p>'
        '<p>Once you signed it, follow the instructions on the registration page to paste your signature.</p>')

        #create an attachment
        with open('random_challenge.txt', 'w') as f:
            f.write(get_random_string(44))
        
        #add the attachment
        with app.open_resource("random_challenge.txt") as fp:
            msg.attach("random_challenge.txt", "text/plain", fp.read())

        mail.send(msg)
        flash(f'A test message was sent to {recipient}.')

        return redirect(url_for('check_email'))

    return render_template('register.html', form=form)


# @app.route('/confirm/', methods=('GET', 'POST'))
# def confirm():

#     form = ConfirmSig()

#     if form.validate_on_submit():

#         profile = {
#             'Public_key': form.public_key.data,
#             'Signature': form.signature.data
#             }

#         #TODO: ADD VERIFICATION PROCEDURE

#         with open("signatures/" + profile['Public_key'], 'w') as file:
#             json.dump(profile, file)

#         return redirect(url_for('success'))

#     return render_template('confirm.html', form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/confirm/', methods=('GET', 'POST'))
def confirm():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('download_file', name=filename))
            return redirect(url_for('success'))

    return render_template('confirm.html')

from flask import send_from_directory

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)


# @app.route('/upload-image', methods=('GET', 'POST'))
# def upload_image():
#     return render_template("upload_image.html")


@app.route('/success/')
def success():
    return render_template('success.html')


@app.route('/check_email/')
def check_email():
    return render_template('check_email.html')