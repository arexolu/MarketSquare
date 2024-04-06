import quart_flask_patch

from quart import (
    Quart, 
    flash, 
    redirect, 
    request, 
    render_template, 
    session
)
from flask_migrate import Migrate
from pydantic import ValidationError

from .base.model import db
from .auth import auth_module
from .contact import contact_module
from .orders import orders_module
from .products import products_module, featured_products
from .users import users_module, bcrypt
from .utils import mailer


app = Quart(__name__)

# path to database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketsquare.db'
# randomly generated secrete key
app.config['SECRET_KEY'] = 'J5GvyAqmbxORzOOvO1uNjsgxcJVfdOrQ'
# mail configurations
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = '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'

db.init_app(app)
migrate = Migrate(app, db)
bcrypt.init_app(app)
mailer.init_app(app)

@app.errorhandler(500)
async def handle_exception(error=None):
    await flash("An internal error occurred during the request to " + request.url)
    return redirect(request.referrer)


@app.errorhandler(ValidationError)
async def handle_validation_errors(errors):
    await flash(errors.errors()[0]["msg"])
    return redirect(request.referrer)


@app.errorhandler(ValueError)
async def handle_value_error(error):
    await flash(str(error))
    return redirect(request.referrer)

@app.errorhandler(404)
async def handle_not_found(error=None):
    return await render_template('404.html', message="Not Found: " + request.url)

app.register_blueprint(auth_module, url_prefix="/auth")
app.register_blueprint(contact_module, url_prefix="/contact")
app.register_blueprint(orders_module, url_prefix="/orders")
app.register_blueprint(products_module, url_prefix="/products")
app.register_blueprint(users_module, url_prefix="/users")

@app.route("/", strict_slashes=False)
async def index():
    user = session.get('user', {})
    products = featured_products()
    return await render_template('index.html', user=user, products=products)

