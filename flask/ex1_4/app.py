from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

# Initialize Bootstrap
bootstrap = Bootstrap(app)

# Define the form class
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired(), Email()], render_kw={"type": "email"})
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    old_name = session.get('name')
    old_email = session.get('email')
    
    if form.validate_on_submit():
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        
        # Store the submitted values in session
        session['name'] = form.name.data
        session['email'] = form.email.data

        # Redirect to refresh the page and show messages
        return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

if __name__ == '__main__':
    app.run(debug=True)
