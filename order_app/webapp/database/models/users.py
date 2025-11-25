from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from webapp.extensions import db, migrate

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)


    def __repr__(self):
        return f"<User(username='{self.username}')>"