from flask import Blueprint, render_template, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

chatbot_bp = Blueprint('chatbot', __name__)

mail = Mail()

YOUR_EMAIL = 'dillingsq2003@gmail.com'
YOUR_PHONE = '281-763-9753'

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
RECIPIENT_PHONE = os.getenv('RECIPIENT_PHONE')

def send_email_notification(name, email, phone, message):
    try:
        subject = f"New Ticket Submitted - {name}"
        body = f"""
A new ticket has been submitted:

Name: {name}
Email: {email}
Phone: {phone or 'Not provided'}

Message:
{message}

Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        msg = Message(
            subject=subject,
            recipients=[YOUR_EMAIL],
            body=body
        )
        mail.send(msg)
        
        confirmation_msg = Message(
            subject="We Received Your Ticket - Spring Virtual Office",
            recipients=[email],
            body=f"""
Hello {name},

Thank you for contacting Spring Virtual Office! We've received your ticket and our team will review it shortly.

Ticket Details:
{message}

We'll get back to you within 24 hours at this email address.

Best regards,
Spring Virtual Office Team
            """
        )
        mail.send(confirmation_msg)
        
        return True, "Email sent successfully"
    except Exception as e:
        print(f"Email error: {str(e)}")
        return False, str(e)

def send_sms_notification(name, email, phone, message):
    try:
        from twilio.rest import Client
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        sms_body = f"""
New ticket from {name}:
Email: {email}
Phone: {phone or 'N/A'}

Message: {message[:100]}...
        """
        
        message_obj = client.messages.create(
            body=sms_body,
            from_=TWILIO_PHONE_NUMBER,
            to=RECIPIENT_PHONE
        )
        
        return True, f"SMS sent"
    except Exception as e:
        print(f"SMS error: {str(e)}")
        return False, str(e)

@chatbot_bp.route('/api/submit-ticket', methods=['POST'])
def submit_ticket():
    try:
        data = request.get_json()
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        message = data.get('message', '').strip()
        
        if not name or not email or not message:
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        if '@' not in email or '.' not in email:
            return jsonify({
                'success': False,
                'error': 'Invalid email address'
            }), 400
        
        email_success, email_msg = send_email_notification(name, email, phone, message)
        sms_success, sms_msg = send_sms_notification(name, email, phone, message)
        
        if email_success or sms_success:
            return jsonify({
                'success': True,
                'message': 'Ticket submitted successfully!',
                'ticket_id': f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send notification'
            }), 500
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chatbot_bp.route('/chat')
def chat():
    return render_template('chat.html')
