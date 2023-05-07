"""Changed users table and added refresh_jwt table

Revision ID: 8a787fbb66d1
Revises: 214ca63e679a
Create Date: 2023-05-06 15:36:03.279862

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8a787fbb66d1"
down_revision = "214ca63e679a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "refresh_jwt",
        sa.Column(
            "id", sa.UUID(), nullable=False, comment="Идентификатор refresh jwt токена"
        ),
        sa.Column(
            "created", sa.DateTime(), nullable=False, comment="Время создания записи"
        ),
        sa.Column("refresh_jti", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_refresh_jwt_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_refresh_jwt")),
        sa.UniqueConstraint("id", name=op.f("uq_refresh_jwt_id")),
    )
    with op.batch_alter_table("refresh_jwt", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_refresh_jwt_refresh_jti"), ["refresh_jti"], unique=False
        )

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created",
                sa.DateTime(),
                nullable=False,
                comment="Время создания записи",
            )
        )
        batch_op.add_column(
            sa.Column(
                "modified",
                sa.DateTime(),
                nullable=True,
                comment="Время изменения записи",
            )
        )
        batch_op.create_unique_constraint(batch_op.f("uq_users_id"), ["id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("uq_users_id"), type_="unique")
        batch_op.drop_column("modified")
        batch_op.drop_column("created")

    with op.batch_alter_table("refresh_jwt", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_refresh_jwt_refresh_jti"))

    op.drop_table("refresh_jwt")
    # ### end Alembic commands ###
