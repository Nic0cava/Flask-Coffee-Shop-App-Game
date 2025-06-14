from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, NumberRange
import os
import random

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'mysecretkey')

#! Form Classes
class StartForm(FlaskForm):
    submit = SubmitField("Start")
#! Asking user to name their coffee shop
class ShopNameForm(FlaskForm):
    name = StringField("Enter Name:")
    submit = SubmitField('Submit')

class OpenForm(FlaskForm):
    submit = SubmitField("Open Shop")

class ContinueForm(FlaskForm):
    continue_submit = SubmitField("Continue")

class ContinueAnywayForm(FlaskForm):
    continue_anyway = SubmitField("Continue Anyway")

class CancelForm(FlaskForm):
    cancel = SubmitField("Cancel")

class BuyForm(FlaskForm):
    buy = SubmitField("Buy Inventory")

class AddToCartForm(FlaskForm):
    coffee_units = IntegerField('Coffee(250g/$16.90): ', validators=[InputRequired(), NumberRange(min=0, max=10)])
    milk_units = IntegerField('Milk(1800ml/$4.24): ', validators=[InputRequired(), NumberRange(min=0, max=10)])
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
#! Static Variables
# Shop Menu:
menu = ['espresso', 'latte', 'cappuccino']
# Recipes 
recipes = {menu[0]:["18g coffee","50ml water","0ml milk"],
           menu[1]:["24g coffee","200ml water","150ml milk"],
           menu[2]:["24g coffee","250ml water","100ml milk"]}
# Coffee Prices:
prices = {menu[0]: 3.65,
          menu[1]: 6.75,
          menu[2]: 5.95}
# Espresso: $3.65
# Latte: $6.75
# Cappuccino: $5.95

#!TODO: Set up a warning alert flash when user clicks 'Restart' link on the nav, tell user that all data will be reset an a new game will begin!

@app.route('/', methods=['GET','POST'])
def start():
    session.pop('name', None)
    #! Changing Variables
    # Starting Balance: $50.00 #! Possibly create a balance_sheet.html page when user clicks on the balance link in the nav
    session['balance'] = 50.00
    # Starting Inventory: coffee(250g), milk(1800ml) #! Create a inventory.html page
    session['inventory'] = {
        'coffee': 250,
        'milk': 1800
    }
    session['random_coffee'] = random.choice(menu)
    session['customer_number'] = 1
    session['named'] = False
    session['accepted'] = False
    form = StartForm()
    if form.validate_on_submit():
        return redirect(url_for('name_shop'))
    return render_template('start.html', form=form)

@app.route('/name_shop', methods=['GET','POST'])
def name_shop():
    session.pop('name', None)
    named = session['named']
    form = ShopNameForm()
    if form.validate_on_submit():
        session['named'] = True
        session['name'] = form.name.data
        return redirect(url_for('open_shop'))
    return render_template('name_shop.html', form=form, named=named)

@app.route('/open_shop', methods=['GET','POST'])
def open_shop():
    form = OpenForm()
    if form.validate_on_submit():
        return redirect(url_for('front_desk'))
    return render_template('open_shop.html', form=form)

@app.route('/close', methods=['GET','POST'])
def close_shop():
    are_you_sure = False
    form = CancelForm()
    form2 = ContinueForm()
    form3 = ContinueAnywayForm()
    if form.cancel.data and form.validate_on_submit():
        return redirect(url_for('front_desk'))
    elif form2.continue_submit.data and form2.validate_on_submit():
        are_you_sure = True
        flash('WARNING: By continuing, all game data will be reset!')
    elif form3.continue_anyway.data and form3.validate_on_submit():
        return redirect(url_for('start'))
    return render_template('close_shop.html', form=form, form2=form2, form3=form3, are_you_sure= are_you_sure)

@app.route('/inventory', methods=['GET','POST'])
def inventory():
    session['cart_total'] = 0.00
    need_inventory = False
    form = BuyForm()
    inventory = session.get('inventory', {'coffee': 0, 'milk': 0})
    coffee = inventory['coffee']
    milk = inventory['milk']
    if form.validate_on_submit():
        need_inventory = True 
        return redirect(url_for('buy_inventory'))
    return render_template('inventory.html', coffee=coffee, milk=milk, form=form, need_inventory=need_inventory)

@app.route('/buy_inventory', methods=['GET','POST'])
def buy_inventory():
    added_to_cart = False
    form = AddToCartForm()
    form2 = ConfirmOrderForm()
    form3 = CancelForm()
    inventory = session.get('inventory', {})
    cart_total = session['cart_total']
    
    if form.validate_on_submit():
        added_to_cart = True
        session['coffee_units'] = form.coffee_units.data
        session['milk_units']  = form.milk_units.data

        # Get Total
        # Coffee(250g/$16.90)
        coffee_cost = session['coffee_units'] * 16.90
        # Milk(1800/$4.24)
        milk_cost = session['milk_units'] * 4.24
        session['cart_total'] = coffee_cost + milk_cost
        cart_total = session['cart_total']
    elif form2.confirm_order.data and form2.validate_on_submit():
        if cart_total > session['balance']:
            flash(f"Insufficient funds: The transfer cannot be completed as there is not enough available balance in your account!", "insufficient")
            return redirect(url_for('buy_inventory'))
        # Update inventory
        inventory['coffee'] += session['coffee_units'] * 250
        inventory['milk'] += session['milk_units'] * 1800
        session['inventory'] = inventory  # Save back to session

        # Update balance
        session['balance'] -= round(cart_total, 2)
        flash(f"Success: Added {session['coffee_units']*250}g coffee and {session['milk_units']*1800}ml milk to inventory.", "sufficient")
        return redirect(url_for('buy_inventory'))
    elif form3.cancel.data and form3.validate_on_submit():
        added_to_cart = False

    coffee = inventory['coffee']
    milk = inventory['milk']
    return render_template('buy_inventory.html', coffee=coffee, milk=milk, form=form, cart_total=cart_total, added_to_cart=added_to_cart, form2=form2, form3=form3)


@app.route('/front_desk', methods=['GET','POST'])
def front_desk():
    accepted = session['accepted']
    rejected = False
    random_coffee = session['random_coffee']
    customer_num = session['customer_number']
    customer_mess = f"Hello, can I have a {random_coffee} please." #! Make a list of each message
    form = RejectForm()
    form2 = MakeCoffeeForm()
    form3 = NextCustomerForm() #! show this after you give coffee also
    form4 = GiveCoffeeForm()
    if form.reject.data and form.validate_on_submit():
        rejected = True
        customer_mess = f"This place sucks :("
    elif form2.make.data and form2.validate_on_submit():
        session['accepted'] = True
        return redirect(url_for('coffee_machine'))
    elif form3.next_customer.data and form3.validate_on_submit():
        rejected = False
        session['random_coffee'] = random.choice(menu)
        session['customer_number'] += 1
        return redirect(url_for('front_desk'))
    elif form4.give.data and form4.validate_on_submit():
        #! check to see if the_made_coffee matches customers order, if not, customer rejects,so make new coffee, else success, Update Balance with added sale
        #! store session['the_made_coffee'] = latte <-- based on user input from CoffeeMachineForm()
        session['accepted'] = False
        return redirect(url_for('front_desk'))
    return render_template('front_desk.html', random_coffee=random_coffee, customer_mess=customer_mess, customer_num=customer_num, form=form, form2=form2, form3=form3, form4=form4, rejected=rejected, accepted=accepted)

@app.route('/coffee_machine', methods=['GET','POST'])
def coffee_machine():
    made = False
    menu_items = []
    for item in menu:
        menu_items.append(item)
    all_ingredients = []
    for ingredients in recipes.values():
        all_ingredients.extend(ingredients)
    form = CoffeeMachineForm()
    form2 = RemakeForm()
    form3 = DoneForm()
    if form.make.data and form.validate_on_submit():
        #! Update Inventory
        #! Check to see what drink was made and store in (if not in recipes, value = None) <-- None will always get rejected by customer
        #! session['the_made_coffee'] = latte
        made = True
    if form2.remake.data and form2.validate_on_submit():
        return redirect(url_for('coffee_machine'))
    if form3.done.data and form3.validate_on_submit():
        return redirect(url_for('front_desk'))
    

    return render_template('coffee_machine.html', menu_items=menu_items, all_ingredients=all_ingredients, form=form, made=made, form2=form2, form3=form3)



if __name__=="__main__":
    app.run(debug=True) #! turn off before deployment