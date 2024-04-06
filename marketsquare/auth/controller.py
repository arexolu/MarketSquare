from quart import (
    Blueprint, 
    flash, 
    redirect, 
    render_template,
    request, 
    session, 
    url_for
)
from sqlalchemy.orm.exc import NoResultFound
from .validators import (
    validate__signin_req,
    validate__forgot_password_req,
    validate__reset_password_req,
)
from ..decorators.logout_required import logout__required
from .model import Auth

mod = Blueprint("auth", __name__)

@mod.route("/", strict_slashes=False)
@logout__required
async def signin():
    form = session.get('form', {})
    return await render_template('signin.html', form=form)

@mod.route("/", methods=["POST"], strict_slashes=False)
@validate__signin_req
async def process_signin():
    try:
        request_data = await request.form
        user = Auth.signin(
            email=request_data.get('email'), 
            password=request_data.get('password')
        )
        session['user'] = user.to_dict()
        del session['form']
        return redirect(url_for('index'))
    except (NoResultFound, ValueError) as e:
        print(str(e))
        await flash('Invalid email or password')
        return redirect(request.referrer)
    except Exception as e:
        print(str(e))
        await flash('An error occured')
        return redirect(request.referrer)

@mod.route("/forgot-password", strict_slashes=False)
@logout__required
async def forgot_password():
    form = session.get('form', {})
    return await render_template('forgot-password.html', form=form)

# Password recovery route
@mod.route("/forgot-password", methods=["POST"], strict_slashes=False)
@validate__forgot_password_req
async def process_forgot_password():
    try:
        request_data = await request.form
        Auth.forgot_password(email=request_data.get("email"))
        session['forgot-password-email'] = request_data.get("email")
        del session['form']
        return redirect(url_for('auth.reset_password'))

    except (ValueError, NoResultFound) as e:
        await flash("User account does not exist")
        return redirect(request.referrer)

    except Exception as e:
        print(str(e))
        await flash("An error occured")
        return redirect(request.referrer)

@mod.route("/passwords", strict_slashes=False)
@logout__required
async def reset_password():
    email = session.get('forgot-password-email', '')
    form = session.get('form', {})
    return await render_template('reset-password.html', email=email, form=form)

# Reset password route
@mod.route("/passwords", methods=["POST"], strict_slashes=False)
@validate__reset_password_req
async def process_reset_password():
    try:
        request_data = await request.form
        Auth.reset_password(
            email=request_data.get('email'),
            password=request_data.get('password'),
            code=request_data.get('code')
        )
        del session['forgot-password-email']
        del session['form']

        await flash('Your password has been reset successfully', "success")
        
        return redirect(url_for('auth.signin'))

    except (NoResultFound, ValueError) as e:
        await flash('Password reset code is invalid')
        return redirect(request.referrer)

    except Exception as e:
        print(str(e))
        await flash("An error occured")
        return redirect(request.referrer)


@mod.route("/signout", strict_slashes=False)
async def signout():
    if session.get('user', None):
        del session['user']
    if session.get('form', None):
        del session['form']
    return redirect(url_for('index'))