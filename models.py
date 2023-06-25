import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import relationship

from extensions import Base


class User(Base):
    __tablename__ = 'flask_user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String, nullable=False, index=True)
    password = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=func.now())


class Advetisement(Base):
    __tablename__ = 'flask_adv'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False, index=True)
    text = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=func.now())
    owner_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    owner = relationship('User', foreign_keys=[owner_id])


Base.metadata.create_all()
