from sqlmodel import Session, select

from database import engine, create_db_and_tables
from models import Task


def seed_database():

    create_db_and_tables()

    with Session(engine) as session:

        if session.exec(select(Task)).first() is None:

            session.add(Task(title="Buy milk", done=False))
            session.add(Task(title="Walk the dog", done=True))
            session.add(Task(title="Finish FlyRank assignment", done=False))

            session.commit()


if __name__ == "__main__":
    seed_database()