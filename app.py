from flask import Flask, render_template, request, redirect, url_for,flash
import mysql.connector
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")
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



# EMAIL FUNCTION (SEND TO OWNER)
def send_email(first, last, sender_email, subject, message):
    print("SEND_EMAIL FUNCTION CALLED")
    
    try:
        owner_email = os.environ.get("OWNER_EMAIL")
        smtp_user = os.environ.get("EMAIL_USER")
        smtp_pass = os.environ.get("EMAIL_PASS")
        print("OWNER_EMAIL =", owner_email)
        print("SMTP_USER =", smtp_user)
        print("SMTP_PASS EXISTS =", bool(smtp_pass))


        if not owner_email or not smtp_user or not smtp_pass:
            print("EMAIL SETTINGS MISSING")
            return

        msg = MIMEText(f"""
New Contact Form Message

Name: {first} {last}
Email: {sender_email}
Subject: {subject}

Message:
{message}
""")

        msg["Subject"] = f"Contact Form: {subject}"
        msg["From"] = owner_email
        msg["To"] = owner_email
        msg["Reply-To"] = sender_email

        print("Trying SMTP connection...")
        print("OWNER_EMAIL =", owner_email)
        print("SMTP_USER =", smtp_user)

        server = smtplib.SMTP(
    "smtp-relay.brevo.com",
    2525,
    timeout=20
)
        print("CONNECTED")
        server.starttls()
        print("TLS OK")
        server.login(smtp_user, smtp_pass)
        print("LOGIN OK")

        server.sendmail(
        smtp_user,
    owner_email,
    msg.as_string()
)
        server.quit()

        print("EMAIL SENT SUCCESS")

    except Exception as e:
        print("EMAIL FAILED:", str(e))


# ==========================
# CONTACT FORM
# ==========================
@app.route('/contact', methods=['POST'])
def contact():
    print("CONTACT ROUTE CALLED")
    try:
        first = request.form['first_name']
        last = request.form['last_name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO contacts
            (first_name, last_name, email, subject, message)
            VALUES (%s, %s, %s, %s, %s)
        """, (first, last, email, subject, message))

        db.commit()

        cursor.close()
        db.close()

        # Email failure won't break the form
        try:
            send_email(first, last, email, subject, message)
        except Exception as email_error:
            print("EMAIL ERROR:", email_error)

        flash("Message submitted successfully!", "success")

        return redirect(url_for('dashboard'))

    except Exception as e:
        print("CONTACT ERROR:", e)

        flash("Something went wrong!", "danger")

        return redirect(url_for('dashboard'))


if __name__ == "__main__":

       app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

