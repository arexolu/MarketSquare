from quart import (
    Blueprint, 
    flash, 
    redirect, 
    request, 
    render_template, 
    session,
    url_for
)
from .model import Order
from .items.model import OrderItem
from .items.validators import validate__order_item_req
from ..products.model import Product
from ..decorators.login_required import login__required
from functools import reduce


mod = Blueprint("orders", __name__)

@mod.route("/", strict_slashes=False)
@login__required
async def list_orders():
    user = session.get('user')
    orders = Order.query.filter(
                    Order.user_id==user['id'],
                    Order.status != 'draft'
                )\
                .order_by(Order.created_at)\
                .all()
    return await render_template('orders.html', 
        orders=orders,
        user=user
    )


@mod.route("/cart", strict_slashes=False)
@login__required
async def show_shopping_cart():
    user = session.get('user')
    cart_order = session.get('active_cart_order', {})
    cart_order = Order.query.filter(
        Order.status == 'draft',
        Order.id == cart_order.get('id')
    ).one_or_none()
    return await render_template('cart.html', cart_order=cart_order, user=user)


@mod.route("/items", methods=['POST'], strict_slashes=False)
@login__required
@validate__order_item_req
async def add_order_item():
    try:

        request_data = await request.form

        product = Product.query.filter(
            Product.id == request_data.get('product_id', type=int),
            Product.units_available > request_data.get('quantity', type=int)
        ).one_or_none()

        if not product:
            await flash("Product cannot be added to cart due to insufficient quantity")
            raise Exception

        user = session.get('user')

        active_cart_order = session.get('active_cart_order', None)

        if not active_cart_order:
            active_cart_order = Order.create(
                user_id = user['id']
            )
        else:
            active_cart_order = Order.query.get(active_cart_order['id'])
        
        amount = product.price * request_data.get('quantity', type=int)

        active_cart_order.order_items.append(
            OrderItem(**request_data, amount=amount)
        )

        active_cart_order.total += amount

        active_cart_order.save()

        session['active_cart_order'] = active_cart_order.to_dict()

        await flash("{} added to cart".format(product.name), "success")
        return redirect(request.referrer)
    except Exception as e:
        print(str(e))
        return redirect(request.referrer)
    

@mod.route("/items/<int:id>", methods=['POST'], strict_slashes=False)
@login__required
@validate__order_item_req
async def update_order_item(id: int):
    try:

        request_data = await request.form

        product = Product.query.filter(
            Product.id == request_data.get('product_id', type=int),
            Product.units_available > request_data.get('quantity', type=int)
        ).one_or_none()

        if not product:
            await flash("Product cannot be added to cart due to insufficient quantity")
            raise Exception

        item = OrderItem.query.get(id)

        item.amount = product.price * request_data.get('quantity', type=int)
        item.quantity = request_data.get('quantity', type=int)
        item.save()

        order = Order.query.get(item.order_id)

        # recalculate the total amount

        amounts = map(lambda x: x.amount, order.order_items)
        order.total = reduce(lambda x, y: x + y, amounts)
        
        order.save()
    
        session['active_cart_order'] = order.to_dict()

        await flash("{} updated".format(product.name), "success")
        return redirect(request.referrer)
    except Exception as e:
        print(str(e))
        return redirect(request.referrer)
    


@mod.route("/checkout", methods=['POST'], strict_slashes=False)
@login__required
async def checkout():
    cart_order = session.get('active_cart_order', None)

    if not cart_order:
        raise Exception

    order = Order.query.get(cart_order['id'])

    order.status = 'new'

    # recalculate the total amount
    amounts = map(lambda x: x.amount, order.order_items)
    order.total = reduce(lambda x, y: x + y, amounts)
    
    ## deduct the product units_available for each order item
    for item in order.order_items:
        item.product.units_available -= item.quantity
        item.product.save()

    order.save()

    del session['active_cart_order']
    await flash("Your order was successful", "success")
    return redirect(url_for('orders.list_orders'))
