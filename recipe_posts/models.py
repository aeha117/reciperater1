"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'recipe',
    Field('recipe_name', requires=IS_NOT_EMPTY()),
    Field('recipe_time', requires=IS_NOT_EMPTY()),
    Field('recipe_content', 'text', requires=IS_NOT_EMPTY()),
    Field('user_email', default=get_user_email),
    Field('recipe_likes', 'integer', requires=IS_INT_IN_RANGE(0, 1e10)),
    Field('recipe_dislikes', 'integer', requires=IS_INT_IN_RANGE(0, 1e10)),
    Field('date_created', 'datetime', default=get_time),
)

db.recipe.id.readable = db.recipe.id.writable = False
db.recipe.user_email.readable = db.recipe.user_email.writable = False
db.recipe.date_created.readable = db.recipe.date_created.writable = False

db.define_table(
    'tags',
    Field('tag_name', requires=IS_NOT_EMPTY()),
    Field('recipe_id', 'reference recipe'),
)

db.define_table(
    'ingredients',
    Field('ingredient_name', requires=IS_NOT_EMPTY()),
    Field('ingredient_amount', 'text', requires=IS_NOT_EMPTY()),
    Field('ingredient_unit'),
    Field('recipe_id', 'reference recipe'),
)

db.define_table(
    'user_bio',
    Field('bio_content', 'text'),
    Field('user_email', default=get_user_email),
)

db.define_table(
    'comments',
    Field('comment_content', 'text'),
    Field('user_email', default=get_user_email),
    Field('name', requires=IS_NOT_EMPTY()),
    Field('likers', type='list:string'),
    Field('dislikers', type='list:string'),
)

db.define_table(
    'replies',
    Field('comment_id', 'reference comments'),
    Field('reply_content', 'text'),
    Field('user_email', default=get_user_email),
    Field('name', requires=IS_NOT_EMPTY()),
)

db.commit()