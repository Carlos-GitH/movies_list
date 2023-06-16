from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

#DATABASE CREATION

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies_database.db'
db = SQLAlchemy()
db.init_app(app)


# DATABASE TABLE STRUTCTURE DECLARATION
class Movies(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String,  unique=True, nullable=False)
    year        = db.Column(db.String,               nullable=True )
    description = db.Column(db.String,  unique=True, nullable=False)
    rating      = db.Column(db.Float,   unique=True, nullable=False)
    ranking     = db.Column(db.Integer,              nullable=False)
    review      = db.Column(db.String,               nullable=False)
    img_url     = db.Column(db.String,  unique=True, nullable=False)

# # DATABASE MOVIES TABLE CREATION    
# with app.app_context():
#     db.create_all()    
# # ADDING FIRST ENTRY TO THE DATABASE    

# new_movie       = Movies(
#     title       = "Phone Booth",
#     year        = 2002,
#     description = "Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating      = 7.3,
#     ranking     = 10,
#     review      = "My favourite character was the caller.",
#     img_url     = "https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()


#DEFINING MOVIE RATING FORM
class RatingForm(FlaskForm):
    rating = FloatField('New rating', validators=[DataRequired()])
    review = StringField('New review', validators=[DataRequired()])
    submit = SubmitField('Done')

    
@app.route("/")
def home():
    with app.app_context():
        all_movies = db.session.execute(db.select(Movies)).scalars()
        return render_template("index.html", movies = all_movies)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = RatingForm()
    if form.validate_on_submit():
        with app.app_context():
            movie = db.session.query(Movies).get(1)
            movie.rating = form.rating.data
            movie.review = form.review.data
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
