from abc import ABC, abstractmethod
from typing import Optional, List

from tasks.schemas import TaskOut, TaskCreate, TaskUpdate


class TaskRepositoryInterface(ABC):
    @abstractmethod
    def get_task(self, task_id: str) -> Optional[TaskOut]:
        pass

    @abstractmethod
    def get_tasks(self) -> List[TaskOut]:
        pass

    @abstractmethod
    def create_task(self, task_create: TaskCreate) -> TaskOut:
        pass

    @abstractmethod
    def update_task(self, task_id: str, task_update: TaskUpdate) -> TaskOut:
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> TaskOut:
        pass
