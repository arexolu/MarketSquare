from quart import (
    Blueprint, 
    flash, 
    redirect, 
    render_template,
    request,
    session
)
from .validators import validate__contact_us_req
from ..utils.mailer import send_message

mod = Blueprint("contact", __name__)

@mod.route("/", strict_slashes=False)
async def contact():
    user = session.get('user', {})
    form = session.get('form', {})
    return await render_template('contact.html', form=form, user=user)

@mod.route("/", methods=['POST'], strict_slashes=False)
@validate__contact_us_req
async def process_contact():
    try:
        request_data = await request.form
        send_message(
            send_to="arexolu@gmail.com",
            subject="Online User Feedback from {}".format(
                request_data.get('name')
            ),
            message=request_data.get("message"),
            reply_to=(
                request_data.get('name'),
                request_data.get('email')
            )
        )
        del session['form']
        await flash("Message received!", "success") 
           
    except Exception as e:
        await flash(str(e))
    
    finally:
        return redirect(request.referrer)