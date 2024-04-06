from quart import (
    Blueprint, 
    flash, 
    redirect, 
    request, 
    render_template, 
    session, 
    url_for
)
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from .model import User
from ..decorators.login_required import login__required
from ..decorators.logout_required import logout__required

from .validators import (
    validate__signup_req,
    validate__update_user_req,
    validate__change_password_req
)

mod = Blueprint("users", __name__)


@mod.route("/", strict_slashes=False)
@logout__required
async def signup():
    form = session.get('form', {})
    return await render_template('signup.html', form=form)


@mod.route("/", methods=["POST"], strict_slashes=False)
@validate__signup_req
async def process_signup():
    try:
        request_data = await request.form
        User.create(**request_data)
        del session['form']
        await flash("Account created successfully", "success")
        return redirect(url_for('auth.signin'))
    
    except IntegrityError:
        await flash("Account with this email exists")
        return redirect(request.referrer)
    except SQLAlchemyError as e:
        print(str(e))
        await flash(str(e))
        return redirect(request.referrer)
    except Exception as e:
        print(str(e))
        await flash(str(e))
        return redirect(request.referrer)


@mod.route("/<int:id>")
@login__required
async def show_user(id: int):
    try:
        user_id = session.get('user')['id']
        if user_id != id:
            raise Exception
        user = User.query.get(id)
        form = session.get('form', user)
        form2 = session.get('form2', {})
        return await render_template('profile.html', user=user, form=form, form2=form2)
    except NoResultFound:
        await flash("User not found")
        raise 404
        # return redirect(url_for())


@mod.route("/<int:id>", methods=["POST"])
@login__required
@validate__update_user_req
async def update_user(id: int):
    try:
        request_data = await request.form
        user_id = session.get('user')['id']
        if user_id != id:
            raise Exception
        user = User.query.get(id)
        user.update(request_data)
        del session['form']
        session['user'] = user.to_dict()
        await flash("User details updated successfully", "success")
    except Exception as e:
        print(str(e))
        await flash("Unable to update user")
    finally:
        return redirect(request.referrer)


# Set password route
@mod.route("/<int:id>/passwords", methods=["POST"])
@login__required
@validate__change_password_req
async def change_password(id: int):
    try:
        request_data = await request.form
        user_id = session.get('user')['id']
        if user_id != id:
            raise Exception

        user = User.query.get(id)

        if not user.has_valid_password(request_data.get('password')):
            await flash("Current password is wrong")
            raise Exception

        user.set_password(password=request_data.get("new_password"))
        user.save()

        del session['form2']
        await flash("Password has been changed successfully", "success")
    
    except Exception as e:
        print(str(e))
        await flash("Unable to change password")
    
    finally:
        return redirect(request.referrer)
