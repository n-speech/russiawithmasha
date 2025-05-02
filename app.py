from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route('/send', methods=['POST'])
def send():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    file = request.files.get('file')

    if not file:
        return jsonify({'error': 'Aucun fichier reçu'}), 400

    # Préparer l'email
    msg = EmailMessage()
    msg['Subject'] = f'Nouveau devoir de {name}'
    msg['From'] = os.environ['SMTP_USER']
    msg['To'] = os.environ['TARGET_EMAIL']
    msg.set_content(f"Nom : {name}\nEmail : {email}\nMessage :\n{message}")

    # Joindre le fichier
    msg.add_attachment(file.read(), maintype='application', subtype='octet-stream', filename=file.filename)

    # Envoyer l'email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ['SMTP_USER'], os.environ['SMTP_PASS'])
            smtp.send_message(msg)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
