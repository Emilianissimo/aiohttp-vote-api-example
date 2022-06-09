import aiopg.sa

from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)

__all__ = [
    'question',
    'choice',
    'posts',
    'pg_context',
]

meta = MetaData()

posts = Table(
    'posts', meta,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('body', String(10000), nullable=False),
    Column('user_id', Integer)
)

question = Table(
    'question', meta,
    Column('id', Integer, primary_key=True),
    Column('question_text', String(255), nullable=False),
    Column('pub_date', Date, nullable=False),
)

choice = Table(
    'choice', meta,
    Column('id', Integer, primary_key=True),
    Column('choice_text', String(200), nullable=False),
    Column('votes', Integer, server_default="0", nullable=False),
    Column('question_id', Integer, ForeignKey('question.id', ondelete='CASCADE'))
)


async def pg_context(app):
    conf = app['configuration']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize']
    )

    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()
