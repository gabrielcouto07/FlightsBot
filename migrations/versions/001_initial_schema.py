"""Initial database schema for Flight Bot"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database tables"""
    
    # Routes table
    op.create_table(
        'routes',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('origin_iata', sa.String(3), nullable=False),
        sa.Column('destination_iata', sa.String(3), nullable=False),
        sa.Column('threshold_price', sa.Float(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_routes_origin_iata'), 'routes', ['origin_iata'], unique=False)
    op.create_index(op.f('ix_routes_destination_iata'), 'routes', ['destination_iata'], unique=False)
    op.create_index(op.f('ix_routes_is_active'), 'routes', ['is_active'], unique=False)
    
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(20), nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('plan', sa.String(), nullable=False, server_default='free'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('phone_number', name='uq_users_phone_number')
    )
    op.create_index(op.f('ix_users_phone_number'), 'users', ['phone_number'], unique=True)
    op.create_index(op.f('ix_users_is_active'), 'users', ['is_active'], unique=False)
    
    # User Alerts table
    op.create_table(
        'user_alerts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('origin_iata', sa.String(3), nullable=True),
        sa.Column('destination_iata', sa.String(3), nullable=True),
        sa.Column('date_from', sa.Date(), nullable=False),
        sa.Column('date_to', sa.Date(), nullable=False),
        sa.Column('max_price', sa.Float(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_alerts_user_id'), 'user_alerts', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_alerts_origin_iata'), 'user_alerts', ['origin_iata'], unique=False)
    op.create_index(op.f('ix_user_alerts_destination_iata'), 'user_alerts', ['destination_iata'], unique=False)
    op.create_index(op.f('ix_user_alerts_is_active'), 'user_alerts', ['is_active'], unique=False)
    
    # Price Snapshots table
    op.create_table(
        'price_snapshots',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('origin', sa.String(3), nullable=False),
        sa.Column('destination', sa.String(3), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False, server_default='BRL'),
        sa.Column('airline', sa.String(255), nullable=False),
        sa.Column('airline_iata', sa.String(2), nullable=True),
        sa.Column('departure_at', sa.DateTime(), nullable=False),
        sa.Column('return_at', sa.DateTime(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('booking_url', sa.String(512), nullable=False),
        sa.Column('deep_link', sa.String(512), nullable=False),
        sa.Column('captured_at', sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_price_snapshots_origin'), 'price_snapshots', ['origin'], unique=False)
    op.create_index(op.f('ix_price_snapshots_destination'), 'price_snapshots', ['destination'], unique=False)
    op.create_index(op.f('ix_price_snapshots_price'), 'price_snapshots', ['price'], unique=False)
    op.create_index(op.f('ix_price_snapshots_airline_iata'), 'price_snapshots', ['airline_iata'], unique=False)
    op.create_index(op.f('ix_price_snapshots_departure_at'), 'price_snapshots', ['departure_at'], unique=False)
    op.create_index(op.f('ix_price_snapshots_captured_at'), 'price_snapshots', ['captured_at'], unique=False)
    
    # Sent Alerts table
    op.create_table(
        'sent_alerts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('snapshot_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('alert_type', sa.String(50), nullable=False),
        sa.Column('sent_at', sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['snapshot_id'], ['price_snapshots.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sent_alerts_snapshot_id'), 'sent_alerts', ['snapshot_id'], unique=False)
    op.create_index(op.f('ix_sent_alerts_user_id'), 'sent_alerts', ['user_id'], unique=False)
    op.create_index(op.f('ix_sent_alerts_alert_type'), 'sent_alerts', ['alert_type'], unique=False)
    op.create_index(op.f('ix_sent_alerts_sent_at'), 'sent_alerts', ['sent_at'], unique=False)


def downgrade() -> None:
    """Drop all tables"""
    op.drop_table('sent_alerts')
    op.drop_table('price_snapshots')
    op.drop_table('user_alerts')
    op.drop_table('users')
    op.drop_table('routes')
