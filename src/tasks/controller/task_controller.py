from fastapi import HTTPException

from tasks.repositories import TaskRepositoryInterface
from tasks.schemas import TaskCreate, TaskUpdate


class TaskController:
    def __init__(self, task_repository: TaskRepositoryInterface):
        self.task_repository = task_repository

    def read_task(self, task_id: str):
        task = self.task_repository.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return task

    def read_tasks(self):
        return self.task_repository.get_tasks()

    def create_task(self, task: TaskCreate):
        return self.task_repository.create_task(task)

    def update_task(self, task_id: str, task: TaskUpdate):
        return self.task_repository.update_task(task_id, task)

    def delete_task(self, task_id: str):
        return self.task_repository.delete_task(task_id)
