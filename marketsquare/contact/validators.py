from pydantic import BaseModel, EmailStr, Field
from quart import current_app, flash, request, redirect, session
from functools import wraps


class ContactUsArgs(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    message: str = Field(min_length=5)


# decorator for validating the request body to /contact
def validate__contact_us_req(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        request_data = await request.form
        session['form'] = request_data

        fields_required = ["name", "email", "message"]
        for field in fields_required:
            if field not in request_data or request_data[field] == "":
                await flash("{} is required".format(field))
                return redirect(request.referrer)

        try:
            ContactUsArgs(**request_data)
            return await current_app.ensure_async(f)(*args, **kwargs)
        except Exception as e:
            print(e.errors()[0])
            await flash("A required field is missing or invalid")
            return redirect(request.referrer)

    return decorated