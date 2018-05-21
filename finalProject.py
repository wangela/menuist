from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


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
        flash("Added {} to our retaurant database!".format(new_name))
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('addrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    output = "This page edits restaurant {}".format(restaurant_id)
    return output

@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    output = "This page deletes restaurant {}".format(restaurant_id)
    return output

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    output = "This page shows the menu for restaurant {}".format(restaurant_id)
    return output

@app.route('/restaurant/<int:restaurant_id>/new/')
def addMenuItem(restaurant_id):
    output = "This page adds an item to the menu for restaurant {}".format(restaurant_id)
    return output

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    output = "This page edits menu item {} for restaurant {}".format(menu_id, restaurant_id)
    return output

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    output = "This page deletes menu item {} for restaurant {}".format(menu_id, restaurant_id)
    return output


if __name__ == '__main__':
    app.secret_key = 'super_duper_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
