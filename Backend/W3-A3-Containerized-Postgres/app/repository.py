from sqlmodel import Session, select

from models import Task


def get_tasks(session: Session):
    return session.exec(select(Task)).all()


def get_task(session: Session, task_id: int):
    return session.get(Task, task_id)


def create_task(session: Session, task: Task):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(session: Session, task: Task):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task: Task):
    session.delete(task)
    session.commit()