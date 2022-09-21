"""Seed database with sample data from CSV Files."""

from csv import DictReader
from app import db
from models import User, Post, Location, Movie

db.drop_all()
db.create_all()

with open('generator/users.csv', encoding='windows-1252') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))

with open('generator/locations.csv', encoding='windows-1252') as locations:
    db.session.bulk_insert_mappings(Location, DictReader(locations))

with open('generator/movies.csv', encoding='windows-1252') as movies:
    db.session.bulk_insert_mappings(Movie, DictReader(movies))

with open('generator/posts.csv', encoding='windows-1252') as posts:
    db.session.bulk_insert_mappings(Post, DictReader(posts))
db.session.commit()
