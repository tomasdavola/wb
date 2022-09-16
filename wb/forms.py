from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalRangeField, MultipleFileField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, ValidationError, NumberRange
from flask_login import current_user


class InputForm(FlaskForm):
    name = StringField('Nombre: (', validators=[InputRequired()])
    email = StringField('Email:')
    tel_num = StringField('Número de telefono: (', validators=[InputRequired()])
    address = StringField('Domicilio: (', validators=[InputRequired()])
    order = StringField('Pedido: (', validators=[InputRequired()])
    file = FileField('Archivo:', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
    mop = SelectField("Método de pago: (", validators=[InputRequired()], choices=["Efectivo (En domicilio)", "Mercado Libre"])

    submit = SubmitField('Submitir pedido')