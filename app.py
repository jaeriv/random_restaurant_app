from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from random_restaurant import generate_restaurant
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
categories = ["American", "Sandwiches", "Fast Food", "Mexican", "Chinese", "Italian",
              "Fine Dining", "Steakhouse", "Pizza", "Japanese", "Indian",
              "Thai", "Pub", "Bar", "Vietnamese", "Other"]

ratings = ["1", "2", "3", "4", "5"]



class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip_code = db.Column(db.String(5), nullable=True)
    category = db.Column(db.String(80), nullable=False)
    contact = db.Column(db.String(12), nullable=True)
    added_by = db.Column(db.String(15), nullable=True)
    website = db.Column(db.String(100), nullable=True)
    rating = db.Column(db.String, nullable=False)


db.create_all()


def random_restaurants():
    if db.session.query(Restaurants).count() != 0:
        random_row = random.randrange(0, db.session.query(Restaurants).count())
        random_restaurant = db.session.query(Restaurants)[random_row]
        return random_restaurant


@app.route('/')
def main():
    random_restaurant = random_restaurants()
    all_locations = db.session.query(Restaurants).all()
    return render_template("main.html", locations=all_locations, random_location=random_restaurant)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_restaurant = Restaurants(name=request.form["restaurant-name"],
                                     address=request.form["address"],
                                     city=request.form["city"],
                                     state=request.form["state"],
                                     zip_code=request.form["zip"],
                                     category=request.form["category"],
                                     contact=request.form["contact"],
                                     added_by=request.form["added-by"],
                                     website=request.form["web-url"],
                                     rating=request.form["rating"])
        db.session.add(new_restaurant)
        db.session.commit()
        return redirect(url_for("main"))
    return render_template("add-location.html", states=states, categories=categories, ratings=ratings)


@app.route("/delete")
def delete():
    restaurant_id = request.args.get("id")
    restaurant_to_delete = Restaurants.query.get(restaurant_id)
    db.session.delete(restaurant_to_delete)
    db.session.commit()
    return redirect(url_for("main"))


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        restaurant_id = request.form["id"]
        restaurant_to_edit = Restaurants.query.get(restaurant_id)
        restaurant_to_edit.rating = request.form["updated-rating"]
        db.session.commit()
        return redirect(url_for("main"))
    restaurant_id = request.args.get("id")
    selected_restaurant = Restaurants.query.get(restaurant_id)
    return render_template("edit.html", restaurant=selected_restaurant, ratings=ratings)


@app.route("/random", methods=["GET", "POST"])
def random_restaurant():
    rating = "none"
    if request.method == "POST":
        try:
            zip_code_entered = request.form["zip-code"]
            restaurant = generate_restaurant(zip_code_entered)
            name = restaurant[0]
            website = restaurant[1]
            category = f"Category: {restaurant[2]}"
            rating = restaurant[3]
            phone_number = restaurant[4]
            address = restaurant[5]
            yelp_link_text = "Yelp Link"
            error_message = restaurant[6]
            return render_template("random.html", name=name, website=website, category=category, rating=rating,
                                   phone_number=phone_number, address=address, yelp_link_text=yelp_link_text,
                                   error_message=error_message)
        except Exception:
            rating = "none"
            error_message = "Sorry, something went wrong. Please try again later or try a different zip code."
            return render_template("random.html", error_message=error_message, rating=rating)

    return render_template("random.html",rating=rating)


if __name__ == '__main__':
    app.run(debug=True)
