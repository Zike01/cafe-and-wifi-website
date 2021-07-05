from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, FloatField
from wtforms.validators import DataRequired, URL
import os
from dotenv import load_dotenv

app = Flask(__name__)
Bootstrap(app)
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL_2",  "sqlite:///cafes.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(500), unique=True, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(50), nullable=False)
    coffee_price = db.Column(db.String(50), nullable=False)


db.create_all()


class AddForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired(), URL(message="Invalid URL")])
    img_url = StringField("Image URL", validators=[DataRequired(), URL(message="Invalid URL")])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField("Has Sockets")
    has_toilet = BooleanField("Has Toilet")
    has_wifi = BooleanField("Has Wifi")
    can_take_calls = BooleanField("Can Take Calls")
    seats = StringField("Number of Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price (£)", validators=[DataRequired()])
    submit = SubmitField("Add Cafe")


@app.route("/")
def home():
    return render_template("index.html", cafes=Cafe.query.all())


@app.route("/add-cafe", methods=["GET", "POST"])
def add_cafe():
    form = AddForm()
    if form.validate_on_submit():
        cafe = Cafe.query.filter_by(name=form.name.data).first()
        
        if cafe:
            flash("That cafe has already been added.", "danger")
            return redirect(url_for('add_cafe'))
        
        
        if "£" not in form.coffee_price.data:
            coffee_price = f"£{form.coffee_price.data}"
        else:
            coffee_price = form.coffee_price.data
        
        new_cafe = Cafe(
            name = form.name.data,
            map_url = form.map_url.data,
            img_url = form.img_url.data,
            location = form.location.data,
            has_sockets = form.has_sockets.data,
            has_toilet = form.has_toilet.data,
            has_wifi = form.has_wifi.data,
            can_take_calls = form.can_take_calls.data,
            seats = form.seats.data,
            coffee_price = coffee_price,
        )
        
        db.session.add(new_cafe)
        db.session.commit()
        flash(f"{new_cafe.name} Added!", "success")
        return redirect(url_for('add_cafe'))
    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
