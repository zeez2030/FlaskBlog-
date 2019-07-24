import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def save_pdf(form_pdf):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pdf.filename)
    pdf_fn = random_hex + f_ext
    pdf_path = os.path.join(
        current_app.root_path, 'static/pdfs', pdf_fn)

    form_pdf.save(pdf_path)
    return pdf_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f''' to reset your password , visit the following link:
    {url_for('users.reset_token' , token=token , _external=True)}
    If you did not make this request then simply ignore this email
    '''
    mail.send(msg)
