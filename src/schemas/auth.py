from pydantic import BaseModel, EmailStr, constr


class UserRegister(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=100)
    full_name: constr(min_length=1, max_length=100) | None = None


    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str



class TokenData(BaseModel):
    user_id: str | None = None
