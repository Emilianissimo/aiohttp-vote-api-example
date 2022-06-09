from aiohttp import web
from app import models
import aiohttp_jinja2 as jinja2

routes = web.RouteTableDef()


async def index(request):
    async with request.app['db'].acquire() as conn:
        query = request.query.get('data')  # get "GET" data
        choices = await conn.execute(models.choice.select())
        choices = await choices.fetchall()
        choices = [dict(c) for c in choices]
    return web.Response(text=str(choices))


@jinja2.template('questions.html')
async def questions(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(models.question.select())
        records = await cursor.fetchall()
        questions = [dict(q) for q in records]
        context = {
            'questions': questions
        }
        return context


@jinja2.template('question.html')
async def question(request):
    async with request.app['db'].acquire() as conn:
        question_id = request.match_info['pk']
        question = await conn.execute(models.question.select().where(models.question.c.id == question_id))
        choices = await conn.execute(models.choice.select().where(models.choice.c.question_id == question_id))
        question = await question.fetchall()
        choices = await choices.fetchall()
        question = [dict(q) for q in question]
        choices = [dict(c) for c in choices]
        context = {
            'question': question[0],
            'choices': choices
        }
        return context


async def create_choice(request):
    async with request.app['db'].acquire() as conn:
        question_id = request.match_info['pk']
        post_data = await request.post()
        await conn.execute(models.choice.insert().values(
            question_id=question_id,
            choice_text=post_data.get('choice_text'))
        )
        raise web.HTTPFound(post_data.get('location'))


@jinja2.template('choice_edit.html')
async def edit_choice(request):
    async with request.app['db'].acquire() as conn:
        choice_id = request.match_info['choice_id']
        choice = await conn.execute(models.choice.select().where(models.choice.c.id == choice_id))
        choice = await choice.fetchall()
        choice = [dict(c) for c in choice]
        context = {
            'choice': choice[0],
        }
        return context


async def update_choice(request):
    async with request.app['db'].acquire() as conn:
        choice_id = request.match_info['choice_id']
        post_data = await request.post()
        await conn.execute(models.choice.update().values(
            choice_text=post_data.get('choice_text')
        ).where(models.choice.c.id == choice_id))
        raise web.HTTPFound(post_data.get('location'))


async def delete_choice(request):
    async with request.app['db'].acquire() as conn:
        choice_id = request.match_info['choice_id']
        post_data = await request.post()
        await conn.execute(models.choice.delete().where(models.choice.c.id == choice_id))
        raise web.HTTPFound(post_data.get('location'))
