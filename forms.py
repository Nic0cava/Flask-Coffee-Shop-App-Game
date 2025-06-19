from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, NumberRange

# Form Classes
class StartForm(FlaskForm):
    submit = SubmitField("Start")

class ShopNameForm(FlaskForm):
    name = StringField("Enter Name:")
    submit = SubmitField('Submit')

class RestartForm(FlaskForm):
    restart = SubmitField('Restart Game')

class OpenForm(FlaskForm):
    submit = SubmitField("Open Shop")

class ContinueForm(FlaskForm):
    continue_submit = SubmitField("Continue")

class ContinueAnywayForm(FlaskForm):
    continue_anyway = SubmitField("Continue Anyway")

class CancelForm(FlaskForm):
    cancel = SubmitField("Cancel")

class ContinuePlayingForm(FlaskForm):
    continue_playing = SubmitField("Continue Playing")

class BuyForm(FlaskForm):
    buy = SubmitField("Buy Inventory")

class AddToCartForm(FlaskForm):
    coffee_units = IntegerField('Coffee(125g/$16.90): ', validators=[InputRequired(), NumberRange(min=0, max=10)])
    milk_units = IntegerField('Milk(600ml/$4.24): ', validators=[InputRequired(), NumberRange(min=0, max=10)])
    add_to_cart = SubmitField("Add To Cart")

class ConfirmOrderForm(FlaskForm):
    confirm_order = SubmitField("Confirm Order")

class MakeCoffeeForm(FlaskForm):
    make = SubmitField("Make Coffee")
class GiveCoffeeForm(FlaskForm):
    give = SubmitField("Give Coffee To Customer")

class CoffeeMachineForm(FlaskForm):
    add_coffee = SelectField(u'Coffee:',choices=[('18g','18g'), ('24g','24g')])
    add_water = SelectField(u'Water:',choices=[('50ml','50ml'), ('200ml','200ml'), ('250ml','250ml')])
    add_milk = SelectField(u'Milk:',choices=[('0ml','0ml'), ('100ml','100ml'), ('150ml','150ml')])
    make = SubmitField("Make")

class RemakeForm(FlaskForm):
    remake = SubmitField("Remake")

class DoneForm(FlaskForm):
    done = SubmitField("Done")

class RejectForm(FlaskForm):
    reject = SubmitField("Reject")

class NextCustomerForm(FlaskForm):
    next_customer = SubmitField("Next Customer")