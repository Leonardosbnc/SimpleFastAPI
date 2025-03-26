from pydantic import BaseModel


class ForgotPassword(BaseModel):
    username: str
