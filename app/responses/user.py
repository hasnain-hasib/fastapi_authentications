from pydantic import EmailStr
from typing import Union
from datetime import datetime
from app.responses.base import BaseResponse

class UserResponse(BaseResponse):
    id: int
    name: str
    email: EmailStr
    created_at: Union[str, None, datetime] = None

