from quart import current_app, session, flash, redirect, request
from functools import wraps

# decorator to ensure user is not logged in
def logout__required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        try:
            user = session.get('user', None)
            if not user:
                return await current_app.ensure_async(f)(*args, **kwargs)
            raise ValueError
        except Exception as e:
            print(str(e))
            await flash("You need to be logged out to continue")
            return redirect(request.referrer)

    return decorated
