# The Game Loop that will be converted into a Flask App
# This file contains a rough draft of the functionality of the application
# Will convert to a Flask app once finished

# My installs:
# pip install Flask
# pip install Flask-WTF
# pip install WTForms
# pip install gunicorn

#! TODOS:
#! Need to add Error Handling
#! Clean and Condense any repetitive code
#! Move functions to separate file

import random
import time
# Ask for Coffee Shop Name
shop_name = input("Congratulations on your new coffee shop! What would you like to name your coffee shop?").capitalize()
print(f"Your shop name is: {shop_name}")

#! Static Variables 
# Shop Menu: #! Could possibly have this be up to the player?
menu = ['espresso', 'latte', 'cappuccino']
# Recipes 
recipes = {menu[0]:"18g coffee, 50ml water, 0ml milk",
           menu[1]:"24g coffee, 200ml water, 150ml milk",
           menu[2]:"24g coffee, 250ml water, 100ml milk"}
# Coffee Prices:
prices = {menu[0]: 3.65,
          menu[1]: 6.75,
          menu[2]: 5.95}
# Espresso: $3.65
# Latte: $6.75
# Cappuccino: $5.95

#! Changing Variables (needs session['variable name'] in Flask)
#! Set at start of the game in Flask app
# Starting Balance: $50.00
balance = 50.00
# Starting Inventory: coffee(250g), milk(1800ml)
coffee = 250
milk = 1800

# Update inventory:
def update_inventory(current_coffee, current_milk, coffee_used, milk_used):
    current_coffee -= coffee_used
    current_milk -= milk_used
    return current_coffee, current_milk

# Update balance
def update_balance(current_balance, revenue):
    current_balance += revenue
    return current_balance

# Buy inventory
def buy_inventory(current_balance, current_coffee, current_milk):
    while True:
        print(f'balance: ${current_balance}')
        print(f"inventory: coffee: {current_coffee}g, milk: {current_milk}ml")
        command = input("What would you like to buy? (commands: buy coffee:'c', buy milk:'m', exit:'e'): ")
        if command == 'c':
            coffee = {'price': 16.90, 'quantity': 250}
            print(f"1 Coffee Bag = {coffee['quantity']}g = ${coffee['price']}")
            coffee_order = int(input("How much coffee would you like to buy? (enter quantity): "))
            amount = coffee_order * coffee['quantity']
            cost = coffee_order * coffee['price']
            current_coffee += amount
            current_balance -= cost
            continue
        elif command == 'm':
            milk = {'price': 4.24, 'quantity': 1800}
            print(f"1 Milk = {milk['quantity']}ml = ${milk['price']}")
            milk_order = int(input("How much milk would you like to buy? (enter quantity): "))
            amount = milk_order * milk['quantity']
            cost = milk_order * milk['price']
            current_milk += amount
            current_balance -= cost
            continue
        elif command == 'e':
            break
        else:
            print('Bad response, try again! Please pick from the list of commands!')
            continue
    return current_balance, current_coffee, current_milk


shop_open = True
while shop_open:
    #! Add a command so user can view the coffee recipes
    command = input('\nWhat would you like to do? (commands: stay open:"open", close shop:"close", view inventory:"i", view balance:"b", buy inventory: "buy"): ').lower()
    if command == 'open':
        pass
    elif command == 'close':
        #! Make a tracker for how many coffees sold
        gross_profit = balance - 50.00
        print(f'Your gross profit is: ${round(gross_profit, 3)}')
        print('Shop is closed! Goodbye!')
        shop_open = False
        break
    elif command == 'i':
        print(f'coffee: {coffee}g, milk: {milk}ml')
        continue
    elif command == 'b':
        print(f'balance: ${balance}')
        continue
    elif command == 'buy':
        balance, coffee, milk = buy_inventory(balance, coffee, milk)
        continue
    else:
        print('Bad response, try again! Please pick from the list of commands!')
        continue
    
    random_coffee = random.choice(menu)
    print(f'Customer: "Hello, can I have a {random_coffee} please."')
    #! Add a command so user can view the coffee recipes
    make = input('Yes or No: ')
    if make == 'yes':
        while True:
            #! Maybe add an attempts mechanic, if player messes up too many times, customer gets mad
            #! Add a command so user can view the coffee recipes
            command = input('Make a {random_coffee}("m"), or View recipes ("r"): ')
            if command == 'r':
                print('------- Recipes ---------')
                for coffee_name, recipe in recipes.items():
                    print(f"{coffee_name.title()}: {recipe}")
            print('------- Coffee Machine ---------')
            add_coffee = int(input('Add Coffee: '))
            add_water = int(input('Add Water: '))
            add_milk = int(input('Add Milk: '))
            print('-'*20)
            print("Brewing", end="")
            for _ in range(5):
                time.sleep(1.0)
                print(".", end="")
            print("\nDone!")
            print('-'*20)


            # Checks if player has enough inventory and allows them to buy more
            if add_coffee > coffee or add_milk > milk:
                command = input("Not enough ingredients in inventory! Need to buy more inventory? (enter:'buy') or type anything to try again: ")
                if command == 'buy':
                    balance, coffee, milk = buy_inventory(balance, coffee, milk)
                    continue
                continue

            # updates inventory after ingredients are used
            coffee, milk = update_inventory(coffee, milk, add_coffee, add_milk)
            if add_coffee == 24:
                if add_water == 200 and add_milk == 150:
                    coffee_made = menu[1]
                    print(f'Here is your {coffee_made}!')
                    if coffee_made == random_coffee:
                        print('Customer: "Thank you!"')
                        balance = update_balance(balance, prices[menu[1]])
                        break
                    else:
                        print(f'Customer: "I asked for a {random_coffee}, not a {coffee_made}? Make me a {random_coffee}!"')
                        continue
                elif add_water == 250 and add_milk == 100:
                    coffee_made = menu[2]
                    print(f'Here is your {coffee_made}!')
                    if coffee_made == random_coffee:
                        print('Customer: "Thank you!"')
                        balance = update_balance(balance, prices[menu[2]])
                        break
                    else:
                        print(f'Customer: "I asked for a {random_coffee}, not a {coffee_made}? Make me a {random_coffee}!"')
                        continue
                else:
                    print(f'Customer: "Ew! This is not how you make a {random_coffee}! Make me another {random_coffee}!"')
                    continue
            elif add_coffee == 18:
                if add_water == 50 and add_milk == 0:
                    coffee_made = menu[0]
                    print(f'Here is your {coffee_made}!')
                    if coffee_made == random_coffee:
                        print('Customer: "Thank you!"')
                        balance = update_balance(balance, prices[menu[0]])
                        break
                    else:
                        print(f'Customer: "I asked for a {random_coffee}, not a {coffee_made}? Make me a {random_coffee}!"')
                        continue
                else:
                    print(f'Customer: "Ew! This is not how you make a {random_coffee}! Make me another {random_coffee}!"')
                    continue
            else:
                print(f'Customer: "Ew! This is not how you make a {random_coffee}! Make me another {random_coffee}!"')
                continue
                
                
    else:
        print('Customer: "This place sucks!" :(')

