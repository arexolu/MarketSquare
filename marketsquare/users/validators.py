from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator
from quart import current_app, request, flash, redirect, session
from functools import wraps
from ..utils import is_strong_password

class SignupArgs(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if not is_strong_password(password=password):
            raise ValueError("Password is too weak")
        return password


# decorator for validating the request body to /auth
def validate__signup_req(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        request_data = await request.form
        session['form'] = request_data

        fields_required = ["first_name", "last_name", "email", "password"]
        for field in fields_required:
            if field not in request_data or request_data[field] == "":
                await flash("{} is required".format(field))
                return redirect(request.referrer)

        try:
            SignupArgs(**request_data)
            return await current_app.ensure_async(f)(*args, **kwargs)
        except Exception as e:
            print(e.errors()[0])
            await flash("A required field is missing or invalid")
            return redirect(request.referrer)

    return decorated


class UpdateUserArgs(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)

# decorator for validating the request body to /auth
def validate__update_user_req(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        request_data = await request.form
        session['form'] = request_data

        fields_required = ["first_name", "last_name"]
        for field in fields_required:
            if field not in request_data or request_data[field] == "":
                await flash("{} is required".format(field))
                return redirect(request.referrer)

        try:
            UpdateUserArgs(**request_data)
            return await current_app.ensure_async(f)(*args, **kwargs)
        except Exception as e:
            # print(e.errors()[0])
            await flash("A required field is missing or invalid")
            return redirect(request.referrer)

    return decorated


class ChangePasswordArgs(BaseModel):
    password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)
    new_password_confirmation: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, password: str) -> str:
        if not is_strong_password(password=password):
            raise ValueError("Password is too weak")
        return password

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'ChangePasswordArgs':
        pw1 = self.new_password
        pw2 = self.new_password_confirmation
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self

# decorator for validating the request body to /passwords
def validate__change_password_req(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        request_data = await request.form
        session['form2'] = request_data

        fields_required = ["password", "new_password", "new_password_confirmation"]
        for field in fields_required:
            if field not in request_data or request_data[field] == "":
                await flash("{} is required".format(field))
                return redirect(request.referrer)

        try:
            ChangePasswordArgs(**request_data)
            return await current_app.ensure_async(f)(*args, **kwargs)
        except Exception as e:
            print(str(e.errors()))
            await flash("Passwords do not match")
            return redirect(request.referrer)

    return decorated
