from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped
from quart_bcrypt import Bcrypt
from ..base.model import BaseSchema, BaseModel, db
from ..utils import random_number

bcrypt = Bcrypt()

class UserSchema(BaseSchema):    
    class Meta:
        additional = (
            "id",
            "first_name",
            "last_name",
            "email",
            "created_at",
            "updated_at",
        )
        name = "user"
        plural_name = "users"


class User(db.Model, BaseModel):

    __schema__ = UserSchema
    
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: str
    password_hash: Mapped[str] = mapped_column(String(200))
    password_reset_code: Mapped[int] = mapped_column(
        Integer, default=random_number, index=True
    )
    
    def __repr__(self):
        return "<User %r: %r %r>" % (self.id, self.first_name, self.email)

    def __init__(self, password: str, **kwargs):
        super().__init__(**kwargs)
        self.set_password(password=password)

    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def has_valid_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def request_password_reset(self):
        self.password_reset_code = random_number()
        db.session.commit()
