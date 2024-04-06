from quart import current_app, session, flash, redirect, request
from functools import wraps
from ..users.model import User


# decorator for verifying user seeion
def login__required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        try:
            user = session.get('user', None)
            if user and User.query.get(user['id']):
                return await current_app.ensure_async(f)(*args, **kwargs)
            raise ValueError
        except Exception as e:
            print(str(e))
            await flash("You need to login to continue")
            return redirect(request.referrer)

    return decorated
