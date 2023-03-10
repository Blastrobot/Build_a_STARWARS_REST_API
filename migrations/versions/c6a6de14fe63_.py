"""empty message

Revision ID: c6a6de14fe63
Revises: 78a52a1d1d4f
Create Date: 2023-01-17 17:57:21.694509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6a6de14fe63'
down_revision = '78a52a1d1d4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_favorite_characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('fav_character_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fav_character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fav_character_id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('user_favorite_planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('fav_planet_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fav_planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fav_planet_id'),
    sa.UniqueConstraint('user_id')
    )
    op.drop_table('favorites')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], name='favorites_character_id_fkey'),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], name='favorites_planet_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorites_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favorites_pkey'),
    sa.UniqueConstraint('character_id', name='favorites_character_id_key'),
    sa.UniqueConstraint('planet_id', name='favorites_planet_id_key'),
    sa.UniqueConstraint('user_id', name='favorites_user_id_key')
    )
    op.drop_table('user_favorite_planets')
    op.drop_table('user_favorite_characters')
    # ### end Alembic commands ###
