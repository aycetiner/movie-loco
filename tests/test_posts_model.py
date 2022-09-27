"""Posts model tests."""

# run these tests like:
#
#    python -m unittest test_posts_model.py

import sys
import os
from unittest import TestCase
from sqlalchemy import exc

#seting up path to import from parent directory.
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from models import db, User, Post, Location, Likes, Movie

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///movie_locations"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for posts."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("testing", "testing@test.com", "password", None)
        u.id = self.uid

        #Adding a location
        l1 = Location(
            lat=37.479710,
            lng=-122.146879,
            address="1 Hacker Way",
            city="Menlo Park",
            state="CA",
            country="US",
            zipcode=94025
        )
        self.lid = 5
        l1.id = self.lid
        
        #adding a movie
        m1 = Movie(
            id=1,
            title="movie_name",
            popularity=3.0,
            poster_path="https://image.tmdb.org/t/p/w500/saHP97rTPS5eLmrLQEcANmKrsFl.jpg",
            release_date="01-01-2001"
        )
        self.mid=12
        m1.id = self.mid

        db.session.add_all([l1, m1])
        db.session.commit()
        
        
        self.u = User.query.get(self.uid)
        self.l1 = Location.query.get(self.lid)
        self.m1 = Movie.query.get(self.mid)

        self.client = app.test_client()



    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_post_model(self):
        """Does basic post model work?"""
        
        p1 = Post(
            title="new location",
            description="new location added",
            image_url="https://cdn.hswstatic.com/gif/10-breathtaking-views-1-orig.jpg",
            user_id=self.uid,
            location_id=self.lid,
            movie_id=self.mid
        )

        db.session.add(p1)
        db.session.commit()
        self.p1=p1

        # Post should have right id and title.
        self.assertEqual(self.p1.id, 1)
        self.assertEqual(self.p1.title, "new location")
        self.assertNotEqual(self.p1.title, "new location1")

    
    def test_like_post(self):
        "Can I like other posts"

        p1 = Post(
            title="new location",
            description="new location added",
            image_url="https://cdn.hswstatic.com/gif/10-breathtaking-views-1-orig.jpg",
            user_id=self.uid,
            location_id=self.lid,
            movie_id=self.mid
        )

        db.session.add(p1)
        db.session.commit()
        self.p1=p1

        #user likes the post
        self.u.likes.append(p1)

        # User should have 1 like and id of that post should be 1.
        self.assertEqual(len(self.u.likes), 1)
        self.assertEqual(self.u.likes[0].id, 1)


    