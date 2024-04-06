from marshmallow import fields
from sqlalchemy import Integer, Float, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship, backref
from typing import List, Literal
from ..base.model import BaseSchema, BaseModel, db
from .items.model import OrderItem

class OrderSchema(BaseSchema):
    order_items = fields.List(
        fields.Nested(
            'OrderItemSchema', 
            only=(
                'id', 
                'product', 
                'quantity', 
                'amount'
            ),
            dump_only=True,
        )
    )
    user = fields.Nested(
        "UserSchema",
        only=(
            "id",
            "first_name",
            "last_name",
            "email",
        ),
        dump_only=True,
    )
    
    class Meta:
        additional = (
            "id",
            "total",
            "status",
            "created_at",
            "updated_at",
        )
        name = "order"
        plural_name = "orders"


class Order(db.Model, BaseModel):
    __schema__ = OrderSchema

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), index=True, nullable=False
    )
    user: Mapped[Literal["User"]] = relationship("User")
    order_items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", backref=backref("order")
    )
    total: Mapped[float] = mapped_column(Float, CheckConstraint("total >= 0"), default=0.00)
    status: Mapped[str] = mapped_column(String, default='draft', nullable=False)
    
    def __repr__(self):
        return "<Order %r: %r %r>" % (self.id, self.status, self.total)
