from datetime import datetime
from typing import Optional, List

from bson import ObjectId
from fastapi import HTTPException
from pymongo import MongoClient

from tasks.repositories import TaskRepositoryInterface
from tasks.schemas import TaskOut, TaskCreate, TaskUpdate


class TaskRepositoryMongo(TaskRepositoryInterface):
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client.task_database
        self.collection = self.db.task_collection

    def get_task(self, task_id: str) -> Optional[TaskOut]:
        task = self.collection.find_one({"_id": ObjectId(task_id)})
        if task:
            return TaskOut(
                id=str(task["_id"]),
                description=task["description"],
                is_completed=task["is_completed"],
                created_at=task["created_at"],
            )
        return None

    def get_tasks(self) -> List[TaskOut]:
        tasks = self.collection.find()
        return [
            TaskOut(
                id=str(task["_id"]),
                description=task["description"],
                is_completed=task["is_completed"],
                created_at=task["created_at"],
            )
            for task in tasks
        ]

    def create_task(self, task_create: TaskCreate) -> TaskOut:
        new_task = {
            "description": task_create.description,
            "is_completed": False,
            "created_at": datetime.utcnow(),
        }
        result = self.collection.insert_one(new_task)
        new_task["_id"] = result.inserted_id
        return TaskOut(
            id=str(new_task["_id"]),
            description=new_task["description"],
            is_completed=new_task["is_completed"],
            created_at=new_task["created_at"],
        )

    def update_task(self, task_id: str, task_update: TaskUpdate) -> TaskOut:
        updates = {}
        if task_update.description:
            updates["description"] = task_update.description
        if task_update.is_completed is not None:
            updates["is_completed"] = task_update.is_completed

        self.collection.update_one({"_id": ObjectId(task_id)}, {"$set": updates})
        updated_task = self.collection.find_one({"_id": ObjectId(task_id)})
        if not updated_task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        return TaskOut(
            id=str(updated_task["_id"]),
            description=updated_task["description"],
            is_completed=updated_task["is_completed"],
            created_at=updated_task["created_at"],
        )

    def delete_task(self, task_id: str) -> TaskOut:
        task = self.collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        self.collection.delete_one({"_id": ObjectId(task_id)})
        return TaskOut(
            id=str(task["_id"]),
            description=task["description"],
            is_completed=task["is_completed"],
            created_at=task["created_at"],
        )
