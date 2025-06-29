from flask import Flask, render_template, session, redirect, url_for, flash
from forms import StartForm, ShopNameForm, RestartForm, OpenForm, ContinueForm, ContinueAnywayForm, CancelForm, ContinuePlayingForm, BuyForm, AddToCartForm, ConfirmOrderForm, MakeCoffeeForm, GiveCoffeeForm, CoffeeMachineForm, RemakeForm, DoneForm, RejectForm, NextCustomerForm
import os
import random

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')

# Static Variables
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

@app.route('/', methods=['GET','POST'])
def start():
    session.pop('name', None)
    # Changing Session Variables
    # Starting Balance: $0.00
    session['balance'] = 0.00
    # Starting Inventory: coffee(125g), milk(600ml)
    session['inventory'] = {
        'coffee': 125,
        'milk': 600
    }
    session['random_coffee'] = random.choice(menu)
    session['customer_number'] = 1
    session['named'] = False
    session['accepted'] = False
    session['the_made_coffee'] = None
    session['sold_coffee'] = False
    session['bankruptcy'] = False
    session["inventory_lockout"] = False
    session['continue_playing'] = False
    session['num_coffees_sold'] = 0
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
        flash('WARNING: By continuing, all game data will be reset!', "close_shop")
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

    if session['bankruptcy'] and session['inventory_lockout']:
        return redirect(url_for('game_over'))
    
    if form.validate_on_submit():
        added_to_cart = True
        session['coffee_units'] = form.coffee_units.data
        session['milk_units']  = form.milk_units.data

        # Coffee(250g/$16.90)
        coffee_cost = session['coffee_units'] * 16.90
        # Milk(1800/$4.24)
        milk_cost = session['milk_units'] * 4.24
        # Get Total
        session['cart_total'] = coffee_cost + milk_cost
        cart_total = session['cart_total']
    elif form2.confirm_order.data and form2.validate_on_submit():
        if cart_total > session['balance']:
            session['bankruptcy'] = True
            flash(f"Insufficient funds: The transfer cannot be completed as there is not enough available balance in your account!", "insufficient")
            return redirect(url_for('buy_inventory'))
        # Update inventory
        inventory['coffee'] += session['coffee_units'] * 125
        inventory['milk'] += session['milk_units'] * 600
        session['inventory'] = inventory  # Save back to session
        session["inventory_lockout"] = False

        # Update balance
        session['balance'] -= round(cart_total, 2)
        flash(f"Success: Added {session['coffee_units']*125}g coffee and {session['milk_units']*600}ml milk to inventory.", "sufficient")
        return redirect(url_for('buy_inventory'))
    elif form3.cancel.data and form3.validate_on_submit():
        added_to_cart = False

    coffee = inventory['coffee']
    milk = inventory['milk']
    return render_template('buy_inventory.html', coffee=coffee, milk=milk, form=form, cart_total=cart_total, added_to_cart=added_to_cart, form2=form2, form3=form3)


@app.route('/front_desk', methods=['GET','POST'])
def front_desk():
    session['sold_coffee'] = False
    accepted = session['accepted']
    rejected = False
    random_coffee = session['random_coffee']
    customer_num = session['customer_number']
    customer_messages = [
        [f"Hello, can I have a {random_coffee} please.",
        f"I'd like a {random_coffee}, thanks.",
        f"Could you make me a {random_coffee}?",
        f"Hey there, one {random_coffee}, please."],
        
        [f"Thank you!",
        f"This is great, thanks!",
        f"Yum! Appreciate it!",
        f"Delicious! Thanks a lot!"],

        [f"This place sucks :(",
        f"Ugh, worst coffee ever...",
        f"I'm never coming back!",
        f"Totally disappointed..."],

        [f"I asked for a {random_coffee}, not a {session['the_made_coffee']}!",
        f"Seriously? I wanted a {random_coffee}, not a {session['the_made_coffee']}!",
        f"Nope, that's not a {random_coffee}!"],
        
        [f"What kind of coffee is this?! Make me {random_coffee}!",
        f"This is terrible! Just give me a {random_coffee}!",
        f"Not what I asked for! I want a {random_coffee}!"]
    ]

    customer_mess = random.choice(customer_messages[0])
    form = RejectForm()
    form2 = MakeCoffeeForm()
    form3 = NextCustomerForm()
    form4 = GiveCoffeeForm()
    if form.reject.data and form.validate_on_submit():
        rejected = True
        customer_mess = random.choice(customer_messages[2])
    elif form2.make.data and form2.validate_on_submit():
        session['accepted'] = True
        return redirect(url_for('coffee_machine'))
    elif form3.next_customer.data and form3.validate_on_submit():
        rejected = False
        session['random_coffee'] = random.choice(menu)
        session['customer_number'] += 1
        return redirect(url_for('front_desk'))
    elif form4.give.data and form4.validate_on_submit():
        if session['the_made_coffee'] == 'mystery':
            customer_mess = random.choice(customer_messages[4])
            session['the_made_coffee'] = None
        elif session['random_coffee'] == session['the_made_coffee']:
            session['sold_coffee'] = True
            customer_mess = random.choice(customer_messages[1])
            session['num_coffees_sold'] += 1

            # Update balance
            if session['the_made_coffee'] == menu[0]:
                session['balance'] += prices[menu[0]]
            elif session['the_made_coffee'] == menu[1]:
                session['balance'] += prices[menu[1]]
            elif session['the_made_coffee'] == menu[2]:
                session['balance'] += prices[menu[2]]

            session['accepted'] = False
            rejected = True
            session['the_made_coffee'] = None

            if session['balance'] >= 50.00 and session['continue_playing'] == False:
                session['customer_number'] += 1
                return redirect(url_for('you_won'))
        else:
            customer_mess = random.choice(customer_messages[3])
            session['the_made_coffee'] = None
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
        session['add_coffee'] = form.add_coffee.data
        session['add_water'] = form.add_water.data
        session['add_milk'] = form.add_milk.data
        added_coffee = int(session['add_coffee'][:-1])
        added_water = int(session['add_water'][:-2])
        added_milk = int(session['add_milk'][:-2])

        # Check if player has enough inventory
        if added_coffee > session['inventory']['coffee'] or added_milk > session['inventory']['milk']:
            session["inventory_lockout"] = True
            flash("Not enough ingredients in inventory! Go to inventory to buy more!", "insufficient_inventory")
            return redirect(url_for('coffee_machine'))

        session['bankruptcy'] = False
        
        # Update Inventory
        session['inventory']['coffee'] -= added_coffee
        session['inventory']['milk'] -= added_milk

        # Check to see what drink was made
        if added_coffee == 18 and added_water == 50 and added_milk == 0:
            session['the_made_coffee'] = 'espresso'
        elif added_coffee == 24 and added_water == 200 and added_milk == 150:
            session['the_made_coffee'] = 'latte'
        elif added_coffee == 24 and added_water == 250 and added_milk == 100:
            session['the_made_coffee'] = 'cappuccino'
        else:
            session['the_made_coffee'] = "mystery"

        made = True
    if form2.remake.data and form2.validate_on_submit():
        session['the_made_coffee'] = None
        return redirect(url_for('coffee_machine'))
    if form3.done.data and form3.validate_on_submit():
        return redirect(url_for('front_desk'))
    

    return render_template('coffee_machine.html', menu_items=menu_items, all_ingredients=all_ingredients, form=form, made=made, form2=form2, form3=form3)

@app.route('/game_over', methods=['GET','POST'])
def game_over():
    form = RestartForm()
    if form.validate_on_submit():
        return redirect(url_for('start'))
    return render_template('game_over.html', form=form)

@app.route('/you_won', methods=['GET','POST'])
def you_won():
    form = RestartForm()
    form2 = ContinuePlayingForm()
    if form.restart.data and form.validate_on_submit():
        return redirect(url_for('start'))
    if form2.continue_playing.data and form2.validate_on_submit():
        session['continue_playing'] = True
        return redirect(url_for('front_desk'))
    return render_template('you_won.html', form=form, form2=form2)


if __name__=="__main__":
    app.run()