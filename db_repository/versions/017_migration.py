from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
flag = Table('flag', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('flag_name', VARCHAR(length=15)),
    Column('flag_value', VARCHAR(length=256)),
    Column('points', INTEGER),
    Column('game_id', VARCHAR(length=64)),
    Column('found', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['flag'].columns['found'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['flag'].columns['found'].create()
