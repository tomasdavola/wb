import json
from flask import Blueprint
from flask import render_template, request, url_for, redirect, flash
from wb.models import Order, User
from wb.forms import InputForm
import json
import cgi
from wb import database, bcrypt
from wb.users.utils import save_picture, send_email, delete_file, save_pdf
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
import flask_mail


main =  Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
@main.route('/pedir', methods=['GET', 'POST'])
def home():

    form = InputForm(meta={'locales': ['es_ES', 'es']})

    if form.validate_on_submit():
        if form.file.data:
            # picture_file = save_picture(form.file.data)
            picture_file = save_pdf(form.file.data)
            picture_file = f"files/{picture_file}"
            order = Order(name=form.name.data, email=form.email.data, tel_num=form.tel_num.data, address=form.address.data, order=form.order.data, mop=form.mop.data, file=picture_file)
        else:
            order = Order(name=form.name.data, email=form.email.data, tel_num=form.tel_num.data, address=form.address.data, order=form.order.data, mop=form.mop.data)
        database.session.add(order)
        database.session.commit()
        if form.email.data:
            try:
                send_email(user=order.email, order=order)
                flash("Pedido completado", category='success')
            except:
                flash("Correo electronico no econtrado", category='danger')
                database.session.delete(order)
                database.session.commit()
        else:
            flash("Pedido completado", category='success')
        return redirect(url_for('main.home'))
    return render_template('home.html', form=form)


@main.route('/pedidos', methods=['GET', 'POST'])
@login_required
def pedidos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_completed=False, is_i_p=False).order_by(Order.date).paginate(per_page=per_page, page=page)
    return render_template('pedidos.html', orders=orders, per_page=per_page)

@main.route('/en_progreso', methods=['GET', 'POST'])
@login_required
def en_progresos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_i_p=True).order_by(Order.date.desc()).paginate(per_page=per_page, page=page)
    return render_template('en_progreso.html', orders=orders, per_page=per_page)

@main.route('/en_progresar/<id>', methods=['GET', 'POST'])
@login_required
def en_progresar(id):
    order = Order.query.get_or_404(id)
    order.is_i_p = True
    order.date_i_p = datetime.now()
    database.session.commit()

    page=request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(is_completed=False, is_i_p=False).order_by(Order.date).paginate(per_page=10, page=page)
    return render_template('pedidos.html', orders=orders)

@main.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    order = Order.query.get_or_404(id)
    delete_file(order.file)
    database.session.delete(order)
    database.session.commit()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_completed=False).order_by(Order.date).paginate(per_page=per_page, page=page)
    return render_template('pedidos.html', orders=orders, per_page=per_page)

@main.route('/delete_all', methods=['GET', 'POST'])
@login_required
def delete_all():
    orders = Order.query.filter_by(is_completed=False)
    for order in orders:
        delete_file(order.file)
        database.session.delete(order)
    database.session.commit()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_completed=False).order_by(Order.date).paginate(per_page=per_page, page=page)
    return render_template('pedidos.html', orders=orders, per_page=per_page)

@main.route('/complete/<id>', methods=['GET', 'POST'])
@login_required
def complete(id):
    order = Order.query.get_or_404(id)
    order.is_completed = True
    order.date_completed = datetime.now()
    delete_file(order.file)
    order.file = ""
    database.session.commit()

    page=request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(is_completed=False).order_by(Order.date).paginate(per_page=10, page=page)
    return render_template('pedidos.html', orders=orders)

@main.route('/complete_all', methods=['GET', 'POST'])
@login_required
def complete_all():
    orders = Order.query.filter_by(is_completed=False)
    for order in orders:
        order.is_completed = True
        order.date_completed = datetime.now()
        delete_file(order.file)
        order.file = ""
    database.session.commit()

    page=request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(is_completed=False).order_by(Order.date).paginate(per_page=10, page=page)
    return render_template('pedidos.html', orders=orders)

@main.route('/epcomplete/<id>', methods=['GET', 'POST'])
@login_required
def epcomplete(id):
    order = Order.query.get_or_404(id)
    order.is_completed = True
    order.date_completed = datetime.now()
    delete_file(order.file)
    order.file = ""
    database.session.commit()

    page=request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(is_i_p=True).order_by(Order.date).paginate(per_page=10, page=page)
    return render_template('en_progreso.html', orders=orders)

@main.route('/epcomplete_all', methods=['GET', 'POST'])
@login_required
def epcomplete_all():
    orders = Order.query.filter_by(is_completed=False, is_i_p=True)
    for order in orders:
        order.is_completed = True
        order.is_i_p = False
        order.date_completed = datetime.now()
        delete_file(order.file)
        order.file = ""
    database.session.commit()

    page=request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(is_i_p=True).order_by(Order.date).paginate(per_page=10, page=page)
    return render_template('en_progreso.html', orders=orders)

@main.route('/completados', methods=['GET', 'POST'])
@login_required
def completados():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_completed=True).order_by(Order.date.desc()).paginate(per_page=per_page, page=page)
    return render_template('completados.html', orders=orders, per_page=per_page)

@main.route('/delete/<id>/c', methods=['GET', 'POST'])
@login_required
def cdelete(id):
    order = Order.query.get_or_404(id)
    database.session.delete(order)
    database.session.commit()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_completed=True).order_by(Order.date.desc()).paginate(per_page=per_page, page=page)
    return render_template('completados.html', orders=orders, per_page=per_page)

@main.route('/cdelete/c/all', methods=['GET', 'POST'])
@login_required
def cdelete_all():
    orders = Order.query.filter_by(is_completed=True)
    for order in orders:
        database.session.delete(order)
        database.session.commit()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_completed=True).order_by(Order.date.desc()).paginate(per_page=per_page, page=page)
    return render_template('completados.html', orders=orders, per_page=per_page)

@main.route('/delete/<id>/ep', methods=['GET', 'POST'])
@login_required
def epdelete(id):
    order = Order.query.get_or_404(id)
    database.session.delete(order)
    database.session.commit()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_i_p=True).order_by(Order.date.desc()).paginate(per_page=per_page, page=page)
    return render_template('en_progreso.html', orders=orders, per_page=per_page)

@main.route('/epdelete/ep/all', methods=['GET', 'POST'])
@login_required
def epdelete_all():
    orders = Order.query.filter_by(is_i_p=True)
    for order in orders:
        database.session.delete(order)
        database.session.commit()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_i_p=True).order_by(Order.date.desc()).paginate(per_page=per_page, page=page)
    return render_template('en_progreso.html', orders=orders, per_page=per_page)

@main.route('/completados/imprimir', methods=['GET', 'POST'])
@login_required
def completados_print():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_completed=True).order_by(Order.date.desc()).paginate(per_page=per_page, page=page)
    return render_template('completados_print.html', orders=orders, per_page=per_page)

@main.route('/en_progreso/imprimir', methods=['GET', 'POST'])
@login_required
def ep_print():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_i_p=True).order_by(Order.date.desc()).paginate(per_page=per_page, page=page)
    return render_template('ep_print.html', orders=orders, per_page=per_page)

@main.route('/pedidos/print', methods=['GET', 'POST'])
@login_required
def pedidos_print():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_completed=False).order_by(Order.date).paginate(per_page=per_page, page=page)
    return render_template('pedidos_print.html', orders=orders, per_page=per_page)

@main.route('/ep_all', methods=['GET', 'POST'])
@login_required
def ep_all():
    orders = Order.query.filter_by(is_completed=False, is_i_p=False)
    for order in orders:
        order.is_i_p = True
        order.date_i_p = datetime.now()
    database.session.commit()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = Order.query.filter_by(is_completed=False, is_i_p=False).order_by(Order.date).paginate(per_page=per_page, page=page)
    return render_template('pedidos.html', orders=orders, per_page=per_page)