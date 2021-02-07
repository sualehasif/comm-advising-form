from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from modules import get_names
import logging

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[validators.InputRequired('Please enter your name.')])
    email = EmailField('Your email', [validators.DataRequired(), validators.Email()])
    advisor_name = StringField('What is your advisor\'s name?', validators=[validators.InputRequired('Please enter your name.')])
    advisor_email = EmailField('What is your advisor\'s email?', [validators.DataRequired(), validators.Email()])
    example = RadioField('Label', choices=[('value','description'),('value_two','whatever')])

    submit = SubmitField('Submit')

class SubmittedForm():
    def __init__(self, 
                name,
                email,
                advisor_name,
                advisor_email):
        self.name = name
        self.email = email
        self.advisor_name = advisor_name
        self.advisor_email = advisor_email

# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        advisor_name = form.advisor_name.data
        advisor_email = form.advisor_email.data

        submitted_form = SubmittedForm(name, email, advisor_name, advisor_email)
        app.logger.info(submitted_form.name)
        # TODO: empty the form field
        # redirect the browser to another route and template
        return render_template('email.html', form=submitted_form)
        # return redirect( url_for('email', name=name) )
        
    else:
        message = "Please correct the fields in red! Let us know if we made a silly mistake at xxx."
    return render_template('index.html', form=form, message=message)

@app.route('/email/<name>')
def email(name):

    # run function to get actor data based on the id in the path
    return render_template('404.html'), 404
    

# 2 routes to handle errors - they have templates too

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# keep this as is
if __name__ == '__main__':
    app.run(debug=False)
