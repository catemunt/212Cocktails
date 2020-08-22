from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
MENUDB = 'menu.db'

def fetchMenu(con):
    burgers = []
    free = '0'
    cur = con.execute('SELECT burger, price FROM burgers WHERE price>=?', (free,))
    for row in cur:
        burgers.append(list(row))

    drinks = []
    cur = con.execute('SELECT drink, price FROM drinks')
    for row in cur:
        drinks.append(list(row))

    sides = []
    cur = con.execute('SELECT side, price FROM sides')
    for row in cur:
        sides.append(list(row))

    ingredients = []
    cur = con.execute('SELECT id, ingredient FROM ingredients')
    for row in cur:
        ingredients.append(list(row))

    return {'burgers':burgers, 'drinks':drinks, 'sides':sides, 'ingredients':ingredients}

@app.route('/')
def index():
    con = sqlite3.connect(MENUDB)
    menu = fetchMenu(con)
    con.close()

    return render_template('index.html',
                            disclaimer='may contain traces of nuts',
                            burgers=menu['burgers'],
                            drinks=menu['drinks'],
                            sides=menu['sides'],
                            ingredients=menu['ingredients']
                            )

# @app.route('/order')
# def order():
#     con = sqlite3.connect(MENUDB)
#     menu = fetchMenu(con)
#     con.close()
#
#     return render_template('order.html',
#                             disclaimer='may contain traces of nuts',
#                             burgers=menu['burgers'],
#                             drinks=menu['drinks'],
#                             sides=menu['sides'],
#                             ingredients=menu['ingredients']
#                             )

@app.route('/confirm', methods=['POST'])
def confirm():
    alcohols = ''
    count = 0

    for k, v in request.form.items():
        # if request.form.[input]:
            # alcohols[input] = request.form[input]
        if count == 0:
            alcohols = alcohols + '(ingredients.id)=' + k
            count +=1
        else:
            alcohols = alcohols + ' OR ' + '(ingredients.id)=' + k


    print(alcohols)

    con = sqlite3.connect(MENUDB)
    menu = fetchMenu(con)
    cur = con.execute('SELECT DISTINCT cocktails.name, cocktails.image FROM ingredients INNER JOIN (cocktails INNER JOIN cocktailIngredients ON cocktails.id = cocktailIngredients.cocktailid) ON ingredients.id = cocktailIngredients.ingredientsid WHERE ((' + alcohols + '))')

    records = cur.fetchall()
    print(records)

    con.close()
    items = {}

    for input in request.form:
        if request.form[input]:
            items[input] = request.form[input]

    print(items)


    return render_template('confirm.html',
                            items = items,
                            records = records)
