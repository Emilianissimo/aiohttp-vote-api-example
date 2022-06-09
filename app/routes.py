from aiohttp import web
from app.api import views, parser, api


def setup_routes(app):
    app.add_routes([
        web.get('/', views.index, name="views.index"),
        web.get('/questions/', views.questions, name="views.questions"),
        web.get('/questions/{pk:\d+}/', views.question, name="views.question"),
        web.post('/questions/{pk:\d+}/create-choice/', views.create_choice, name="views.create_choice"),
        web.get("/questions/{pk:\d+}/choice/{choice_id:\d+}/", views.edit_choice, name="views.edit_choice"),
        web.post('/questions/{pk:\d+}/choice/{choice_id:\d+}/update/', views.update_choice, name="views.update_choice"),
        web.post('/questions/{pk:\d+}/choice/{choice_id:\d+}/delete/', views.delete_choice, name="views.delete_choice"),

        # Api routes

        web.get('/api/', api.index, name="api.index"),

        web.get('/api/questions/', api.questions, name="api.questions"),
        web.post('/api/questions/', api.create_question, name="api.question.create"),

        web.get('/api/questions/{pk:\d+}/', api.question, name="api.question"),
        web.patch('/api/questions/{pk:\d+}/', api.update_question, name="api.question.update"),
        web.delete('/api/questions/{pk:\d+}/', api.delete_question, name="api.question.delete"),

        web.get('/api/choices/', api.choices, name="api.choices"),
        web.post('/api/choices/', api.create_choice, name="api.choices.create"),
        web.patch('/api/choices/{pk:\d+}/', api.update_choice, name="api.choices.update"),
        web.delete('/api/choices/{pk:\d+}/', api.delete_choice, name="api.choices.delete"),

        # Parser

        web.get('/parser/', parser.index, name="parser.index"),
        web.get('/parser/insert-posts/', parser.bind_data, name="parser.posts"),
    ])
