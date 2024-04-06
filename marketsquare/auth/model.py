from ..users.model import User
from ..utils import send_message

class Auth():

    @classmethod
    def signin(cls, email: str, password: str):
        user = User.query.filter_by(email=email).one()
        if user.has_valid_password(password=password):            
            return user
        raise ValueError
     
    @classmethod
    def forgot_password(cls, email: str):
        user = User.query.filter_by(email=email).one()
        user.request_password_reset()
        send_message(
            send_to=email,
            subject="Password Reset Code",
            message="""
            Use code {} to reset your password 
            """.format(user.password_reset_code)
        )
        return user
    
    @classmethod
    def reset_password(cls, email: str, password: str, code: str):
        user = User.query.filter_by(
            email=email,
            password_reset_code=code,
        ).one()
        user.set_password(password)
        user.save()
        return user
