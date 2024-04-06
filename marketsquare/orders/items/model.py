from marshmallow import fields
from sqlalchemy import Integer, Float, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import Literal
from ...base.model import BaseSchema, BaseModel, db


class OrderItemSchema(BaseSchema):
    product = fields.Nested(
        'ProductSchema', 
        only=('id', 'name', 'price'),
        dump_only=True
    )
    
    class Meta:
        additional = (
            "id",
            "product_id",
            "quantity",
            "amount",
        )
        name = "order"
        plural_name = "orders"


class OrderItem(db.Model, BaseModel):
    __schema__ = OrderItemSchema

    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("order.id"), index=True, nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product.id"), index=True, nullable=False
    )
    product: Mapped[Literal["Product"]] = relationship("Product") 
    quantity: Mapped[int] = mapped_column(Integer, CheckConstraint("quantity > 0"), default=1)
    amount: Mapped[float] = mapped_column(Float, CheckConstraint("amount >= 0"), default=0.00)

    UniqueConstraint('order_id', 'product_id', name="unique_product_order_item")
    
    def __repr__(self):
        return "<OrderItem %r: %r %r>" % (self.product_id, self.quantity, self.amount)
