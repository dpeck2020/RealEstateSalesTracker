"""Initial migration; create property table

Revision ID: 446d5ba994bb
Revises: 
Create Date: 2025-03-31 22:11:12.794141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '446d5ba994bb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('property',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('street', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=10), nullable=True),
    sa.Column('zip_code', sa.String(length=20), nullable=True),
    sa.Column('sale_price', sa.Integer(), nullable=True),
    sa.Column('sale_date', sa.Date(), nullable=True),
    sa.Column('lot_size', sa.Float(), nullable=True),
    sa.Column('square_footage', sa.Integer(), nullable=True),
    sa.Column('image_url', sa.String(length=512), nullable=True),
    sa.Column('buyer_name', sa.String(length=255), nullable=True),
    sa.Column('seller_name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_property_city'), ['city'], unique=False)
        batch_op.create_index(batch_op.f('ix_property_sale_date'), ['sale_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_property_state'), ['state'], unique=False)
        batch_op.create_index(batch_op.f('ix_property_street'), ['street'], unique=False)
        batch_op.create_index(batch_op.f('ix_property_zip_code'), ['zip_code'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_property_zip_code'))
        batch_op.drop_index(batch_op.f('ix_property_street'))
        batch_op.drop_index(batch_op.f('ix_property_state'))
        batch_op.drop_index(batch_op.f('ix_property_sale_date'))
        batch_op.drop_index(batch_op.f('ix_property_city'))

    op.drop_table('property')
    # ### end Alembic commands ###
