from pydantic import BaseModel


class UserDto(BaseModel):
    id: int
    name: str
