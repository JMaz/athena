from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
game = Table('game', post_meta,
    Column('game_name', String(length=64), primary_key=True, nullable=False),
    Column('game_description', String(length=64)),
)

score = Table('score', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('score', Integer),
    Column('timestamp', DateTime),
    Column('user_id', String(length=64)),
    Column('game_id', String(length=64)),
)

user = Table('user', pre_meta,
    Column('displayname', VARCHAR(length=64), primary_key=True, nullable=False),
    Column('email', VARCHAR(length=120)),
    Column('firstname', VARCHAR(length=64)),
    Column('lastname', VARCHAR(length=64)),
)

user = Table('user', post_meta,
    Column('display_name', String(length=64), primary_key=True, nullable=False),
    Column('email', String(length=120)),
    Column('firstname', String(length=64)),
    Column('lastname', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['game'].create()
    post_meta.tables['score'].create()
    pre_meta.tables['user'].columns['displayname'].drop()
    post_meta.tables['user'].columns['display_name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['game'].drop()
    post_meta.tables['score'].drop()
    pre_meta.tables['user'].columns['displayname'].create()
    post_meta.tables['user'].columns['display_name'].drop()
