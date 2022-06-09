from datetime import datetime

import psycopg2

from app import models
from aiohttp import web
import json
routes = web.RouteTableDef()


async def index(request):
    query = request.query.get('data')  # get "GET" data
    data = {
        'questions': str(request.url) + 'questions/',
        'choices': str(request.url) + 'choices/',
    }
    return web.json_response(data)


async def questions(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(models.question.select())
        records = await cursor.fetchall()
        questions = [dict(q) for q in records]

        for question in questions:
            question.update({'url': str(request.url) + str(question['id']) + '/'})

        return web.Response(text=json.dumps(questions, indent=4, sort_keys=True, default=str))


async def question(request):
    async with request.app['db'].acquire() as conn:
        question_id = request.match_info['pk']
        question = await conn.execute(models.question.select().where(models.question.c.id == question_id))
        choices = await conn.execute(models.choice.select().where(models.choice.c.question_id == question_id))
        question = await question.fetchall()
        choices = await choices.fetchall()
        question = [dict(q) for q in question]
        choices = [dict(c) for c in choices]

        for choice in choices:
            choice.update({'url': request.scheme + "://" + request.host + '/api/choices/' + str(choice['id']) + '/'})

        question[0].update({'choices': choices})
        return web.Response(text=json.dumps(question[0], indent=4, sort_keys=True, default=str))


async def create_question(request):
    async with request.app['db'].acquire() as conn:
        post_data = await request.json()
        try:
            await conn.execute(models.question.insert().values(
                question_text=post_data.get('question_text'),
                pub_date=datetime.now()
            ))
            return web.json_response(status=201)
        except psycopg2.errors.ForeignKeyViolation:
            return web.json_response({"msg": "Please, check your values"}, status=422)
        except psycopg2.errors.NotNullViolation:
            return web.json_response({"msg": "Please, pass question_text"}, status=400)


async def update_question(request):
    async with request.app['db'].acquire() as conn:
        question_id = request.match_info['pk']
        post_data = await request.json()
        if post_data.get('question_text'):
            await conn.execute(models.question.update().values(
                question_text=post_data.get('question_text')
            ).where(models.question.c.id == question_id))
        return web.json_response(status=204)


async def delete_question(request):
    async with request.app['db'].acquire() as conn:
        question_id = request.match_info['pk']
        await conn.execute(models.question.delete().where(models.question.c.id == question_id))
        return web.json_response(status=204)


async def choices(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(models.choice.select())
        records = await cursor.fetchall()
        choices = [dict(q) for q in records]

        for choice in choices:
            choice.update({'url': str(request.url) + str(choice['id']) + '/'})

        return web.Response(text=json.dumps(choices, indent=4, sort_keys=True, default=str))


async def create_choice(request):
    async with request.app['db'].acquire() as conn:
        post_data = await request.json()
        try:
            await conn.execute(models.choice.insert().values(
                question_id=post_data.get('question_id'),
                choice_text=post_data.get('choice_text')
            ))
            return web.json_response(status=201)
        except psycopg2.errors.ForeignKeyViolation:
            return web.json_response({"msg": "Please check your values"}, status=422)
        except psycopg2.errors.NotNullViolation:
            return web.json_response({"msg": "Please, pass question_id AND choice_text"}, status=400)


async def update_choice(request):
    async with request.app['db'].acquire() as conn:
        choice_id = request.match_info['pk']
        post_data = await request.json()
        if post_data.get('choice_text'):
            await conn.execute(models.choice.update().values(
                choice_text=post_data.get('choice_text')
            ).where(models.choice.c.id == choice_id))
        if post_data.get('question_id'):
            try:
                await conn.execute(models.choice.update().values(
                    question_id=post_data.get('question_id')
                ).where(models.choice.c.id == choice_id))
            except psycopg2.errors.ForeignKeyViolation:
                return web.json_response({"msg": "Please check your values"}, status=422)
        return web.json_response(status=204)


async def delete_choice(request):
    async with request.app['db'].acquire() as conn:
        choice_id = request.match_info['pk']
        await conn.execute(models.choice.delete().where(models.choice.c.id == choice_id))
        return web.json_response(status=204)
