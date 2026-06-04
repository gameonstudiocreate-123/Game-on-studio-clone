from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# MySQL
def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=27546,
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        ssl_ca="ca.pem"
    )


@app.route('/')
def dashboard():
    return render_template('dashboard.html')
# @app.route('/home')
# def home():
#     return render_template('home.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# @app.route('/course')
# def course():
#     return render_template('course.html')

@app.route('/unreal')
def unreal():
    return render_template('unreal.html')
@app.route('/unity')
def unity():
    return render_template('unity.html')

import mysql.connector
import smtplib
from email.mime.text import MIMEText






# EMAIL FUNCTION (SEND TO OWNER)
def send_email(first, last, user_email, subject, message):
    sender_email = "gameonstudiocreate@gmail.com"
    sender_password = "xdbrknghdygqcrrs"

    owner_email = "gameonstudiocreate@gmail.com"   # ✅ YOUR EMAIL

    body = f"""
    New Contact Form Submission:

    Name: {first} {last}
    Email: {user_email}
    Subject: {subject}
    Message: {message}
    """

    msg = MIMEText(body)
    msg["Subject"] = "New Contact Form Submission"
    msg["From"] = sender_email
    msg["To"] = owner_email
    msg["Reply-To"] = user_email   # 🔥 reply goes to user

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()





@app.route('/contact', methods=['POST'])
def contact():
    try:
        first = request.form['first_name']
        last = request.form['last_name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO contacts (first_name, last_name, email, subject, message)
            VALUES (%s, %s, %s, %s, %s)
        """, (first, last, email, subject, message))

        db.commit()
        cursor.close()
        db.close()

        send_email(first, last, email, subject, message)

        return redirect(url_for('dashboard') + "#contact")

    except Exception as e:
       return str(e), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

