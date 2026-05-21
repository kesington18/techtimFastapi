from fastapi import FastAPI, HTTPException, UploadFile, Form, Depends, File
from src.schemas import PostCreate
from src.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession, result
from contextlib import asynccontextmanager
from sqlalchemy import  select

# use for starting up the database immediately the server starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)  # ← lifespan must be passed here

# for uploading files
@app.post("upload")
async def upload_file(
        file: UploadFile = File(...),
        caption: str = Form(""),
        session: AsyncSession = Depends(get_async_session)
):
    post = Post(
        caption=caption,
        url="dummy url",
        file_type="photo",
        file_name="dummy name"
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@app.get("/feed")
async def get_feed(
        session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption" : post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at
            }
        )

    return {
        "posts": posts_data
    }
'''
text_posts = {
    1: {"title": "New Post", "content": "Cool test post"},
    2: {"title": "Python Tip", "content": "Use list comprehensions for cleaner loops."},
    3: {"title": "Daily Motivation", "content": "Consistency beats intensity every time."},
    4: {"title": "Fun Fact", "content": "The first computer bug was an actual moth found in a Harvard Mark II."},
    5: {"title": "Update", "content": "Just launched my new project! Excited to share more soon."},
    6: {"title": "Tech Insight", "content": "Async IO in Python can massively speed up I/O-bound tasks."},
    7: {"title": "Quote", "content": "Programs must be written for people to read, and only incidentally for machines to execute."},
    8: {"title": "Weekend Plans", "content": "Might finally clean up my GitHub repos... or just play some Minecraft."},
    9: {"title": "Question", "content": "What's the most underrated Python library you've ever used?"},
    10: {"title": "Mini Announcement", "content": "New video drops tomorrow—covering the weirdest Python features!"},
    11: {"title": "Coding Hot Take", "content": "Writing clean code is better than writing clever code."},
    12: {"title": "Debugging Life", "content": "That moment when you fix a bug by deleting the code you spent 3 hours writing."},
    13: {"title": "Design Pattern", "content": "Don't over-engineer early on. Keep your architecture simple until it hurts."},
    14: {"title": "Learning Curve", "content": "Starting a new framework always feels like learning to walk all over again."},
    15: {"title": "Productivity Hack", "content": "If a task takes less than two minutes, do it immediately."},
    16: {"title": "Git Reminder", "content": "Always pull before you push to save yourself from avoidable merge conflicts."},
    17: {"title": "Coffee Status", "content": "Converting caffeine into code at an alarming rate today."},
    18: {"title": "Database Tip", "content": "Indexes are your best friend for read-heavy APIs. Use them wisely."},
    19: {"title": "Tech Milestone", "content": "Just hit 100 stars on my open-source project! Incredibly grateful."},
    20: {"title": "Final Thought", "content": "The best error message is the one that never has a reason to show up."}
}

@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_a_post(id: int):
    if id not in text_posts:
        return HTTPException(status_code=404, detail="Post not found")

    return text_posts.get(id)

@app.post("/posts")
def create_post(post: PostCreate) -> PostCreate:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return  new_post
'''

