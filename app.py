from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import os
import random

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'mysecretkey')

#! Asking user to name their coffee shop
class ShopNameForm(FlaskForm):
    name = StringField("Enter Name:")
    submit = SubmitField('Submit')

# @app.route("/")
# def home():
#     return render_template('base.html')

@app.route('/', methods=['GET','POST'])
def start():
    form = ShopNameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('front_desk'))
    return render_template('start.html', form=form)

@app.route('/front_desk')
def front_desk():
    return render_template('front_desk.html')



if __name__=="__main__":
    app.run(debug=True)