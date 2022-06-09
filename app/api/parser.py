import json
import aiohttp
from app import  models
from aiohttp import web


async def index(request):
    async with aiohttp.ClientSession() as session:
        # Getting 100 posts
        async with session.get('https://jsonplaceholder.typicode.com/posts') as response:
            posts = await response.text()
        # Posting one new comment for the first post
        async with session.post('https://jsonplaceholder.typicode.com/posts/1/comments', json={
            "postId": 1,
            "name": "Emilianissimo",
            "email": "Fourteen@fourfour.youknow",
            "body": "Huy there!"
        }) as response:
            comment = await response.text()
        # Getting all comments for this post
        async with session.get('https://jsonplaceholder.typicode.com/posts/1/comments') as response:
            comments = await response.text()
        await session.close()

    posts = json.loads(posts)
    comment = json.loads(comment)
    comments = json.loads(comments)

    data = {
        "posts": posts,
        "comments": comments,
        "new_comment": comment
    }
    return web.Response(text=json.dumps(data))


async def bind_data(request):
    # Getting 100 posts
    async with aiohttp.ClientSession() as session:
        async with session.get('https://jsonplaceholder.typicode.com/posts') as response:
            api_posts = await response.text()
            api_posts = json.loads(api_posts)
        await session.close()
    # Writing all this posts into database
    async with request.app['db'].acquire() as conn:
        for post in api_posts:
            await conn.execute(models.posts.insert().values(
                title=post['title'],
                body=post['body'],
                user_id=post['userId']
            ))

        db_posts = await conn.execute(models.posts.select())
        db_posts = await db_posts.fetchall()
        db_posts = [dict(p) for p in db_posts]

    return web.Response(text=json.dumps(db_posts))
