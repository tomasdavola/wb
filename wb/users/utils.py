import os
import secrets
from PIL import Image
from flask import current_app
from flask_mail import Message
from wb import mail
from flask import url_for, flash, redirect
from wb.models import Post
from wb import database
from flask import render_template

def save_picture(form_picture):
    # if current_img != 'images/default.png':
    #     path=os.path.join(current_app.root_path, current_img)
    #     if os.path.exists(path):
    #         os.remove(path)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/files', picture_fn)

    preferred_size = (900, 900)
    i = Image.open(form_picture)
    i = i.convert('RGB')
    i.thumbnail(preferred_size)
    i.save(picture_path)
    return picture_fn

def delete_file(file):
    file = f"static/{file}"
    path = os.path.join(current_app.root_path, file)
    if os.path.exists(path):
        os.remove(path)

def save_pdf(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, 'static/files', file_fn)
    file.save(file_path)
    return file_fn


def send_email(user, order):

    msg = Message(f"Pedido Recibido. {order.date.strftime('%d %b %Y %H:%M')}", sender=("Farmacia Rodriguez", "tt2413682@gmail.com"), recipients=[user])
    msg.body = f"""¡Gracias por su pedido de Farmacia Rodriguez! Sí hay un problema nos contactaremos contigo.
    \n\n
    Tú pedido:
    {order.order}
    \n
    Farmacia Rodriguez
    4769-0428/4769-3151
    Whatsapp:
    11-6572-3803
    """
    mail.send(msg)
