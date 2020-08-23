from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
MENUDB = 'menu.db'

def fetchMenu(con):
    ingredients = []
    cur = con.execute('SELECT id, ingredient FROM ingredients')
    for row in cur:
        ingredients.append(list(row))

    return {'ingredients':ingredients}

@app.route('/')
def index():
    con = sqlite3.connect(MENUDB)
    menu = fetchMenu(con)
    con.close()

    return render_template('index.html',
                            ingredients=menu['ingredients']
                            )


@app.route('/confirm', methods=['POST'])
def confirm():
    alcohols = ''
    count = 0

    for k, v in request.form.items():
        if count == 0:
            alcohols = alcohols + '(ingredients.id)=' + k
            count +=1
        else:
            alcohols = alcohols + ' OR ' + '(ingredients.id)=' + k


    print(alcohols)

    if alcohols == '':
        print('no selection')
        return redirect(url_for('index')) #render_template('login.html')

    else:
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
