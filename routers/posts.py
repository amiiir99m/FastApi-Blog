from fastapi import APIRouter, Body, Depends
from schema.input import PostInput, UpdatePostInput
from db.engine import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from operations.posts import PostOperation
from schema.jwt import JWTPayload
from utils.jwt import JWTHandler
import os
import uuid

router = APIRouter()


@router.post("/create_post/")
async def create_new_post(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data=Depends(PostInput),
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
    ):
    upload_folder = "C:/Users/user/Desktop/FastApi-blog/static"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_uuid = uuid.uuid4()
    file_name = f"{file_uuid}.{str(data.file.filename).split('.')[-1]}"
    file_path = os.path.join(upload_folder, file_name)
    contents = await data.file.read()  
    with open(file_path, "wb") as buffer:
        buffer.write(contents)   
    image_url = "/static/" + file_name

    post = await PostOperation(db_session).create(data.title, data.description, token_data.username, image_url)

    return post


@router.put("/update_post")
async def update_post(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    old_title:str = Body(),
    update_data= Depends(UpdatePostInput),
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    upload_folder = "C:/Users/user/Desktop/FastApi-blog/static"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        
    if update_data.new_file:
        file_uuid = uuid.uuid4()
        file_name = f"{file_uuid}.{str(update_data.new_file.filename).split('.')[-1]}"
        file_path = os.path.join(upload_folder, file_name)
        contents = await update_data.new_file.read()  
        with open(file_path, "wb") as buffer:
            buffer.write(contents)   
        image_url = "/static/" + file_name
    else:
        image_url = ""

    user = await PostOperation(db_session).update(
        old_title=old_title, author=token_data.username,
        new_title = update_data.new_title, new_description = update_data.new_description, new_image_url= image_url,
    )

    return user


@router.delete("/")
async def delete_post(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    title:str = Body(),
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    await PostOperation(db_session).delete(title, token_data.username)


@router.get('/{title}')
async def get_post_by_title(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    title: str,
):
    post = await PostOperation(db_session).get_post_by_title(title)

    return post


@router.get('/{author}/')
async def get_posts_by_author(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    author:str,
    #title:str
):
    posts = await PostOperation(db_session).get_post_by_author(author)

    return posts


@router.get('/')
async def get_all_posts(
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    posts = await PostOperation(db_session).get_all_posts()

    return posts
