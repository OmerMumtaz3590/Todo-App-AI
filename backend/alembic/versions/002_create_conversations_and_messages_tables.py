"""create conversations and messages tables

Revision ID: 002
Revises: 001
Create Date: 2026-02-04

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create conversations table (MCP-040)
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'],
            name='fk_conversations_user_id',
            ondelete='CASCADE',
        ),
    )
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'])

    # Create messages table (MCP-041)
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ['conversation_id'], ['conversations.id'],
            name='fk_messages_conversation_id',
            ondelete='CASCADE',
        ),
    )
    op.create_index('ix_messages_conversation_id', 'messages', ['conversation_id'])

    # Create trigger on conversations table for updated_at
    # Reuses the update_updated_at_column() function from migration 001
    op.execute("""
        CREATE TRIGGER update_conversations_updated_at
            BEFORE UPDATE ON conversations
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    # Drop trigger
    op.execute("DROP TRIGGER IF EXISTS update_conversations_updated_at ON conversations;")

    # Drop tables
    op.drop_index('ix_messages_conversation_id', 'messages')
    op.drop_table('messages')
    op.drop_index('ix_conversations_user_id', 'conversations')
    op.drop_table('conversations')
