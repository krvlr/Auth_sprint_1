"""create users table

Revision ID: 214ca63e679a
Revises:
Create Date: 2023-04-30 12:09:39.270469

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "214ca63e679a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False, comment="Идентификатор пользователя"),
        sa.Column("login", sa.String(length=256), nullable=False, comment="Логин пользователя"),
        sa.Column(
            "email",
            sa.String(length=320),
            nullable=False,
            comment="Адрес электронной почты пользователя",
        ),
        sa.Column(
            "password_hash",
            sa.String(length=128),
            nullable=False,
            comment="Хэш пароля пользователя",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("id", name=op.f("uq_users_id")),
    )
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_users_login"), ["login"], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_users_login"))

    op.drop_table("users")
    # ### end Alembic commands ###
