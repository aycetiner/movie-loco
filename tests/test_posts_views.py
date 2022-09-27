"""Post View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_posts_views.py

import sys
import os
from unittest import TestCase

#seting up path to import from parent directory.
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from models import db, connect_db, Post, User, Likes, Movie, Location

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///movie_locations"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class PostViewTestCase(TestCase):
    """Test views for posts."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Post.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        # self.l1 = Location(
        #     lat=37.479710,
        #     lng=-122.146879,
        #     address="1 Hacker Way",
        #     city="Menlo Park",
        #     state="CA",
        #     country="US",
        #     zipcode=94025
        # )
        
        # self.l1.id = 105

        self.m1 = Movie(
            id=100,
            title="movie_name",
            popularity=3.0,
            poster_path="https://image.tmdb.org/t/p/w500/saHP97rTPS5eLmrLQEcANmKrsFl.jpg",
            release_date="01-01-2001"
        )

        db.session.add(self.m1)

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp


    def test_add_post(self):
        """Can we add a post?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/posts/new/100", data={
                "title": "test post", 
                "description":"nice test post", 
                "lat":37.479710,
                "lng":-122.146879,
                "address":"1 Hacker Way",
                "city":"Menlo Park",
                "state":"CA",
                "country":"US",
                "zipcode":94025,
                "image_url":"https://media-cdn.tripadvisor.com/media/photo-s/10/c4/23/16/highland-view-bed-and.jpg"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            post = Post.query.one()
            self.assertEqual(post.title, "test post")
            self.assertEqual(post.location.lat, 37.479710)
            self.assertEqual(post.movie.title, "movie_name")

