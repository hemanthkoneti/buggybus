import imp
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField,PasswordField,
                     IntegerField,TextAreaField,RadioField)
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed
from wtforms.fields.html5 import DateField

class JourneyForm(FlaskForm):
    
    from_city=StringField('From City',validators=[DataRequired()])
    to_city=StringField('To City',validators=[DataRequired()])
    date=DateField('Date',validators=[DataRequired()])
    submit=SubmitField('Submit')

class SelectionForm(FlaskForm):
    pass
    
class LoginForm(FlaskForm):
    user_id=StringField('User ID',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')
    
class RegisterForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    phone=StringField('Phone',validators=[DataRequired()])
    DOB=DateField('DOB',validators=[DataRequired()])
    # gender=RadioField(u'Gender',validators=[DataRequired()],choices=[('Male','Male'),('Female','Female'),('Prefer Not to Answer'),('Prefer Not to Answer')])
    # country=RadioField(u'Country',validators=[DataRequired()],choices=[('India','India'),('Bangladesh','Bangladesh'),('Sri Lanka','Sri Lanka'),('Choice4','Choice4')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit=SubmitField('Submit')
    

class ContactForm(FlaskForm):
    phone=IntegerField('Phone',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired()])
    query=TextAreaField('Query')
    submit=SubmitField('Submit')
    