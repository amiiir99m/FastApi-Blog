from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Post
from sqlalchemy.exc import IntegrityError
from exceptions import PostAlreadyExists, PostNotFound
from sqlalchemy.exc import IntegrityError
import sqlalchemy as sa



class PostOperation:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
    
    async def create(self, title:str, description:str, author:str, image_url:str) -> Post:
        post = Post(title=title, description=description, author=author, image_url=image_url)

        async with self.db_session as session:
            try:
                session.add(post)
                await session.commit()
            except IntegrityError:
                raise PostAlreadyExists

        return post
    
    async def update(
            self, old_title:str, author:str,
            new_title:str, new_description:str, new_image_url:str | None = None,
    ) -> Post:
        if new_title is None and new_description is None and new_image_url is None:
            return 
        
        query = sa.select(Post).where(Post.title == old_title, Post.author==author)
        update_values = {}        
        update_values['title'] = new_title
        if new_description is not None and "":
            update_values['description'] = new_description
        if new_image_url is not None and "":
            update_values['image_url'] = new_image_url
        
        update_query = sa.update(Post).where(
            Post.title == old_title,
        ).values(**update_values)

        async with self.db_session as session:
            post_data = await session.scalar(query)

            if post_data is None:
                raise PostNotFound
            
            await session.execute(update_query)
            await session.commit()
            
            return post_data

    async def delete(self, author:str, title:str) -> None:
        query = sa.select(Post).where(Post.author == author, Post.title == title)
        delete_query = sa.delete(Post).where(Post.author == author, Post.title == title) #type: ignore

        async with self.db_session as session:
            post_data = await session.scalar(query)
            if post_data is None:
                raise PostNotFound

            await session.execute(delete_query)
            await session.commit()


    async def get_post_by_title(self, title:str) -> Post:
        query = sa.select(Post).where(Post.title == title)

        async with self.db_session as session:
            post_data = await session.scalar(query)

            if post_data is None:
                raise PostNotFound
            
            return post_data
        

    async def get_post_by_author(self, author:str) -> list[Post]:
        query = sa.select(Post).where(Post.author == author)

        async with self.db_session as session:
            post_data = await session.execute(query)
            datas = [post for post, in post_data]

            if post_data is None:
                raise PostNotFound

            return datas

    async def get_all_posts(self) -> list[Post]:
        query = sa.select(Post)

        async with self.db_session as session:
            post_data = await session.execute(query)
            datas = [post for post, in post_data]

            if post_data is None:
                raise PostNotFound

            return datas

