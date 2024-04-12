from fastapi import FastAPI
import uvicorn
from db.engine import Base, engine
from routers.users import router as user_router
from routers.posts import router as post_router
from fastapi.staticfiles import StaticFiles



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user_router, prefix="/users")
app.include_router(post_router, prefix="/posts")


if __name__ == "__main__":
    uvicorn.run(app)

