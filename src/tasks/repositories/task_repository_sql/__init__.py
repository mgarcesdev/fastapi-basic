from datetime import datetime
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from tasks.repositories import TaskRepositoryInterface
from tasks.repositories.task_repository_sql.task_model_orm import Task
from tasks.schemas import TaskOut, TaskCreate, TaskUpdate


class TaskRepositorySql(TaskRepositoryInterface):
    def __init__(self, engine: Engine):
        self.sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db = self.sessionLocal()

    def get_task(self, task_id: str) -> Optional[TaskOut]:
        task = self.db.query(Task).filter(Task.id == int(task_id)).first()
        if task:
            return TaskOut(
                id=str(task.id),
                description=task.description,
                is_completed=task.is_completed,
                created_at=task.created_at,
            )
        return None

    def get_tasks(self) -> List[TaskOut]:
        tasks = self.db.query(Task).all()
        return [
            TaskOut(
                id=str(task.id),
                description=task.description,
                is_completed=task.is_completed,
                created_at=task.created_at,
            )
            for task in tasks
        ]

    def create_task(self, task_create: TaskCreate) -> TaskOut:
        new_task = Task(
            description=task_create.description,
            is_completed=False,
            created_at=datetime.utcnow(),
        )
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return TaskOut(
            id=str(new_task.id),
            description=new_task.description,
            is_completed=new_task.is_completed,
            created_at=new_task.created_at,
        )

    def update_task(self, task_id: str, task_update: TaskUpdate) -> TaskOut:
        task = self.db.query(Task).filter(Task.id == int(task_id)).first()
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        if task_update.description:
            task.description = task_update.description
        if task_update.is_completed is not None:
            task.is_completed = task_update.is_completed

        self.db.commit()
        self.db.refresh(task)
        return TaskOut(
            id=str(task.id),
            description=task.description,
            is_completed=task.is_completed,
            created_at=task.created_at,
        )

    def delete_task(self, task_id: str) -> TaskOut:
        task = self.db.query(Task).filter(Task.id == int(task_id)).first()
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        self.db.delete(task)
        self.db.commit()
        return TaskOut(
            id=str(task.id),
            description=task.description,
            is_completed=task.is_completed,
            created_at=task.created_at,
        )
