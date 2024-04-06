from pydantic import BaseModel, EmailStr, Field, field_validator
from quart import current_app, request, flash, redirect, session
from functools import wraps
from ..utils import is_strong_password

class SigninArgs(BaseModel):
    email: EmailStr
    password: str


# decorator for validating the request body to /auth
def validate__signin_req(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        request_data = await request.form
        session['form'] = request_data

        fields_required = ["email", "password"]
        for field in fields_required:
            if field not in request_data or request_data[field] == "":
                await flash("{} is required".format(field))
                return redirect(request.referrer)

        try:
            SigninArgs(**request_data)
            return await current_app.ensure_async(f)(*args, **kwargs)
        except Exception as e:
            # print(e.errors()[0])
            await flash("Email or password is invalid")
            return redirect(request.referrer)

    return decorated


class ForgotPasswordArgs(BaseModel):
    email: EmailStr


# decorator for validating the request body to /reset-password
def validate__forgot_password_req(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        request_data = await request.form
        session['form'] = request_data

        if "email" not in request_data or request_data["email"] == "":
            await flash("Email is required")
            return redirect(request.referrer)

        try:
            ForgotPasswordArgs(**request_data)
            return await current_app.ensure_async(f)(*args, **kwargs)
        except Exception as e:
            print(str(e))
            await flash("Email is invalid")
            return redirect(request.referrer)

    return decorated


class ResetPasswordArgs(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    code: str = Field(pattern=r"^\d{6}$", strict=False)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not is_strong_password(password=password):
            raise ValueError("Password is too weak")
        return password


# decorator for validating the request body to /passwords
def validate__reset_password_req(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        request_data = await request.form
        session['form'] = request_data

        fields_required = ["email", "password", "code"]
        for field in fields_required:
            if field not in request_data or request_data[field] == "":
                await flash("{} is required".format(field))
                return redirect(request.referrer)

        try:
            ResetPasswordArgs(**request_data)
            return await current_app.ensure_async(f)(*args, **kwargs)
        except Exception as e:
            print(str(e.errors()))
            await flash("A required field is missing or invalid")
            return redirect(request.referrer)

    return decorated
