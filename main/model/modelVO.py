from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    username: str
    password: str
    userid: Optional[str] = None
    email: Optional[EmailStr] = None
    verified: Optional[bool] = None
    disabled: Optional[bool] = None

    def to_dict_with_empty_string(self):
        user_dict = self.dict()
        for key, value in user_dict.items():
            if value is None:
                user_dict[key] = ""
        return user_dict