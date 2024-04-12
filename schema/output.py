from uuid import UUID

from pydantic import BaseModel


class RegisterOutput(BaseModel):
    username: str
    id: UUID


class PostOutput(BaseModel):
    title: str
    user: str
    id: UUID