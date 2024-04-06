from sqlalchemy import Integer, Float, String, Text, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped
from ..base.model import BaseSchema, BaseModel, db


class ProductSchema(BaseSchema):
    class Meta:
        additional = (
            "id",
            "name",
            "description",
            "image",
            "price",
            "units_available",
            "created_at",
            "updated_at",
        )
        name = "product"
        plural_name = "products"


class Product(db.Model, BaseModel):
    __schema__ = ProductSchema

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=True)
    units_available: Mapped[int] = mapped_column(Integer, CheckConstraint("units_available >= 0"), default=0)
    price: Mapped[float] = mapped_column(Float, CheckConstraint("price >= 0"), default=0.00)
    
    def __repr__(self):
        return "<Product %r: %r %r>" % (self.id, self.name, self.price)
