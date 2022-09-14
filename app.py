import os

from flask import Flask, render_template, request, flash, redirect, session, g
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError


from forms import PostForm, UserAddForm, LoginForm, ProfileEditForm, ChangePasswordForm
from models import db, connect_db, User, Post, Likes, Location, Movie

MovieAPIKey='6461108259d95817ace0a23e57345c98'
GoogleAPIKey = 'AIzaSyCp1jKqmi89h2mhNsKtSZYK3-IT3xEq8go'
MOVIE_API_BASE_URL='https://api.themoviedb.org/3/movie'


CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///movie_locations'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)



def check_auth(f):
    def wrapper(*args, **kwargs):
        if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect("/")
        val = f(*args, **kwargs)
        return val
    wrapper.__name__ = f.__name__
    return wrapper

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash(f" You're logged out. Goodbye!", "success")
    return redirect("/")


##############################################################################
# General user routes:

@app.route('/users')
@check_auth
def list_users():
    """Page with listing of users.

    Can take a 'q' param in querystring to search by that username.
    """

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/index.html', users=users)


@app.route('/users/<int:user_id>')
@check_auth
def users_show(user_id):
    """Show user profile."""
        
    user = User.query.get_or_404(user_id)

    # snagging messages in order from the database;
    # user.messages won't be in order by default
    posts = (Post
                .query
                .filter(Post.user_id == user_id)
                .order_by(Post.created_at.desc())
                .limit(100)
                .all())
    return render_template('users/show.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/likes')
@check_auth
def users_likes(user_id):
    """Show list of followers of this user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/likes.html', user=user)



@app.route('/users/profile', methods=["GET", "POST"])
@check_auth
def edit_profile():
    """Update profile for current user."""

    user = g.user
    form = ProfileEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            try:

                user.username = form.username.data
                user.email = form.email.data
                user.image_url = form.image_url.data
                user.bio = form.bio.data
                  
                db.session.commit()

            except IntegrityError:
                flash("Username already taken", 'danger')
                return render_template('users/edit.html', form=form)

            return redirect(f"/users/{g.user.id}")
        
        else:
            flash("Incorrect Password", 'danger')
            return render_template('users/edit.html', form=form)

    else:
        return render_template('users/edit.html', form=form)



@app.route('/users/profile/password', methods=["GET", "POST"])
@check_auth
def change_password():
    """Change password for current user."""

    user = g.user
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if (form.new_password.data != form.new_password_match.data):
            flash("Non Matching Password", 'danger')
            return render_template('users/edit_password.html', form=form)

        elif User.authenticate(user.username, form.password.data): 
            try:

                new_password = form.new_password.data
                
                user = User.edit_password(user.username, new_password)
                g.user.password = user.password

            except IntegrityError:
                flash("Username already taken", 'danger')
                return render_template('users/edit_password.html', form=form)

            return redirect(f"/users/{g.user.id}")
        
        else:
            flash("Incorrect Password", 'danger')
            return render_template('users/edit_password.html', form=form)

    else:
        return render_template('users/edit_password.html', form=form)




@app.route('/users/delete', methods=["POST"])
@check_auth
def delete_user():
    """Delete user."""

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")


@app.route('/users/add_like/<int:post_id>', methods=["POST"])
@check_auth
def like_post(post_id):
    """Like a post."""

    likes = [like.id for like in g.user.likes]
    if post_id not in likes:
        like = Likes(user_id=g.user.id, post_id=post_id)

        db.session.add(like)

        db.session.commit()

    else:
        like = Likes.query.filter(Likes.user_id==g.user.id, Likes.post_id==post_id).first()
        
        db.session.delete(like)
        db.session.commit()
    

    return redirect("/")


##############################################################################
# Posts routes:
@app.route('/posts/movie_search', methods=["GET", "POST"])
@check_auth
def choose_movie():
    """Choose the movie to add post for:
    """

    # form = PostForm()

    # if form.validate_on_submit():
    #     post = Post(title=form.title.data, description=form.description.data, image_url=form.image_url.data, location_id=form.location_id.data, movie_id=form.movie_id.data)
    #     g.user.posts.append(post)
    #     db.session.commit()

    #     return redirect(f"/users/{g.user.id}")

    return render_template('posts/movie_search.html')



@app.route('/posts/new/<int:movie_id>', methods=["GET", "POST"])
@check_auth
def posts_add(movie_id):
    """Add a post:
    Show form if GET. If valid, update posts and redirect to user page.
    """
    movie = Movie.query.get(movie_id)
    if not movie:
        try:
            new_movie_json = requests.get(f"{MOVIE_API_BASE_URL}/{movie_id}?api_key={MovieAPIKey}&language=en-US").json()

            movie = Movie(
            id=new_movie_json['id'],
            popularity=new_movie_json['popularity'],
            poster_path=new_movie_json['poster_path'],
            title=new_movie_json['title'], 
            release_date=new_movie_json['release_date']
            )
        except:
            render_template('404.html')
    
    form = PostForm()

    if form.validate_on_submit():
        location = Location(
            lat=form.lat.data, 
            lng=form.lng.data, 
            address=form.address.data,  
            city=form.city.data,
            state=form.state.data,
            country=form.country.data,
            zipcode=form.zipcode.data
            )        
        db.session.add(location)
        db.session.add(movie)
        db.session.commit()
        new_location = Location.query.filter_by(lat=form.lat.data, lng=form.lng.data).first()

        


        post = Post(
            title=form.title.data, 
            description=form.description.data, 
            image_url=form.image_url.data,
            location_id=new_location.id, 
            movie_id=movie_id
            )

        g.user.posts.append(post)
        db.session.commit()

        return redirect(f"/users/{g.user.id}")

    return render_template('posts/new.html', form=form, movie=movie)


@app.route('/posts/<int:post_id>', methods=["GET"])
@check_auth
def posts_show(post_id):
    """Show a post."""

    post = Post.query.get(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def post_destroy(post_id):
    """Delete a post."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")


##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no posts
    - logged in: 100 most recent posts
    """

    if g.user:
        posts = (Post
                    .query
                    .order_by(Post.created_at.desc())
                    .limit(100)
                    .all())
        

        likes = [like.id for like in g.user.likes]

        return render_template('home.html', posts=posts, likes=likes)

    else:
        return render_template('home-anon.html')


##############################################################################
# Turning off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req

@app.errorhandler(404)
def page_not_found(e):
    #snip
    return render_template('404.html'), 404



@app.route('/geolocation', methods=["GET", "POST"])
@check_auth
def geolocation():
    """Choose the movie to add post for:
    """

    return render_template('geolocation.html')

# @app.route('/geolocation2', methods=["GET", "POST"])
# @check_auth
# def geolocation2():
#     """Choose the movie to add post for:
#     """

#     return render_template('googmaps.html')