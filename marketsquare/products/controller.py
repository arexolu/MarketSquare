from quart import Blueprint, render_template, session
from sqlalchemy.sql.expression import func
from .model import Product

mod = Blueprint("products", __name__)


@mod.route("/", strict_slashes=False)
async def list_products():
    user = session.get('user', {})
    try:
        products = Product.query.filter(
                        Product.units_available>0
                    )\
                    .order_by(Product.created_at)\
                    .all()
        return await render_template('products.html', 
            products=products,
            user=user
        )
    except Exception as e:
        return await render_template('products.html', 
            error="No products found",
            user=user
        )


def featured_products():
    products = Product.query.filter(
                    Product.units_available>0
                )\
                .order_by(func.random())\
                .limit(3)\
                .all()
    return products
        