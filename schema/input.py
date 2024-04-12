from pydantic import BaseModel
from fastapi import UploadFile, File, Body
from typing import Optional

class UserInput(BaseModel):
    username: str
    password: str


class UpdateUserProfileInput(BaseModel):
    new_username: str


class TaskInput(BaseModel):
    title: str


class TaskUpdateInput(BaseModel):
    old_title: str
    new_title: str


class PostInput:
    def __init__(self, title:str = Body(), description:str= Body(), file:UploadFile = File()):
        self.title = title
        self.description = description
        self.file = file


class UpdatePostInput:
    def __init__(
            self, new_title: Optional[str] = Body(), new_description:Optional[str] = Body(None),
            new_file: bytes = File(default="")
            ):
        self.new_title = new_title
        self.new_description = new_description
        self.new_file = new_file
