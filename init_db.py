from sqlalchemy import create_engine, MetaData

from app.models import question, choice, posts
from configuration.settings import config

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(db_engine):
    meta_data = MetaData()
    meta_data.create_all(bind=db_engine, tables=[question, choice])


def seeder(db_engine):
    conn = db_engine.connect()
    conn.execute(question.insert(), [
        {'question_text': 'What\'s up?',
         'pub_date': '2015-12-15 17:17:49.629+02'}
    ])
    conn.execute(choice.insert(), [
        {'choice_text': 'Not much', 'votes': 0, 'question_id': 1},
        {'choice_text': 'The sky', 'votes': 0, 'question_id': 1},
        {'choice_text': 'Just hacking again', 'votes': 0, 'question_id': 1},
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    # Comment after using first time
    create_tables(engine)
    seeder(engine)

    meta = MetaData()
    meta.create_all(bind=engine, tables=[posts])
