"""Add Phase V fields to Todo table

Revision ID: 003
Revises: 002
Create Date: 2026-02-05 11:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add priority column (enum)
    priority_enum = postgresql.ENUM('HIGH', 'MEDIUM', 'LOW', name='priority_enum')
    priority_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('todos', sa.Column('priority',
                                  sa.Enum('HIGH', 'MEDIUM', 'LOW', name='priority_enum'),
                                  server_default='MEDIUM',
                                  nullable=True))

    # Add tags column (array of strings)
    op.add_column('todos', sa.Column('tags',
                                  postgresql.ARRAY(sa.String()),
                                  server_default='{}',
                                  nullable=True))

    # Add due_date column
    op.add_column('todos', sa.Column('due_date', sa.DateTime(), nullable=True))

    # Add remind_at column
    op.add_column('todos', sa.Column('remind_at', sa.DateTime(), nullable=True))

    # Add recurrence_rule column
    op.add_column('todos', sa.Column('recurrence_rule', sa.String(length=500), nullable=True))

    # Add next_occurrence column
    op.add_column('todos', sa.Column('next_occurrence', sa.DateTime(), nullable=True))

    # Add parent_task_id column for recurring tasks
    op.add_column('todos', sa.Column('parent_task_id', sa.Uuid(), nullable=True))

    # Add foreign key constraint for parent_task_id
    op.create_foreign_key('fk_todos_parent_task_id', 'todos', 'todos',
                          ['parent_task_id'], ['id'])


def downgrade() -> None:
    # Drop foreign key constraint first
    op.drop_constraint('fk_todos_parent_task_id', 'todos', type_='foreignkey')

    # Drop columns
    op.drop_column('todos', 'parent_task_id')
    op.drop_column('todos', 'next_occurrence')
    op.drop_column('todos', 'recurrence_rule')
    op.drop_column('todos', 'remind_at')
    op.drop_column('todos', 'due_date')
    op.drop_column('todos', 'tags')
    op.drop_column('todos', 'priority')

    # Drop enum type
    priority_enum = postgresql.ENUM(name='priority_enum')
    priority_enum.drop(op.get_bind(), checkfirst=True)