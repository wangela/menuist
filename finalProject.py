from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Support API requests (GET request)
@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/JSON')
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/JSON')
def showMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).first()
    return jsonify(MenuItem = item.serialize)

# Regular routing
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def addRestaurant():
    if request.method == 'POST':
        new_name = request.form['name']
        new_restaurant = Restaurant(name = new_name)
        session.add(new_restaurant)
        session.commit()
        flash("Added {} to our restaurant database!".format(new_name))
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('addrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    # output = "This page edits restaurant {}".format(restaurant_id)
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    flashMessage = ""
    if request.method == 'POST':
        if request.form['name']:
            old_name = restaurant.name
            new_name = request.form['name']
            restaurant.name = new_name
            flashMessage += "Renamed {} to {}.".format(old_name, new_name)
        session.add(restaurant)
        session.commit()
        if flashMessage:
            flash(flashMessage)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editrestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    # output = "This page deletes restaurant {}".format(restaurant_id)
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    if request.method == 'POST':
        old_name = restaurant.name
        session.delete(restaurant)
        session.commit()
        flash("Successfully deleted {} from Menuist.".format(old_name))
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    # output = "This page shows the menu for restaurant {}".format(restaurant_id)
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def addMenuItem(restaurant_id):
    # output = "This page adds an item to the menu for restaurant {}".format(restaurant_id)
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        new_name = request.form['name']
        new_description = request.form['description']
        new_price = request.form['price']
        new_item = MenuItem(name = new_name, description = new_description, price = new_price, restaurant_id = restaurant_id)
        session.add(new_item)
        session.commit()
        flash("Added {} to the menu. Sounds delicious!".format(new_name))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('addmenuitem.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    # output = "This page edits menu item {} for restaurant {}".format(menu_id, restaurant_id)
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    item = session.query(MenuItem).filter_by(id = menu_id).first()
    if request.method == 'POST':
        old_name = item.name
        if request.form['name']:
            new_name = request.form['name']
            item.name = new_name
            flash("Renamed {} to {} on the menu.".format(old_name, new_name))
        if request.form['description']:
            new_description = request.form['description']
            item.description = new_description
            flash("Updated description.")
        if request.form['price']:
            new_price = request.form['price']
            item.price = new_price
            flash("Updated price.")
        session.add(item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant = restaurant, item = item)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    # output = "This page deletes menu item {} for restaurant {}".format(menu_id, restaurant_id)
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    item = session.query(MenuItem).filter_by(id = menu_id).first()
    if request.method == 'POST':
        old_name = item.name
        session.delete(item)
        session.commit()
        flash("Deleted {} from the {} menu.".format(old_name, restaurant.name))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant = restaurant, item = item)


if __name__ == '__main__':
    app.secret_key = 'super_duper_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
