from typing import List

from fastapi import APIRouter, HTTPException, Depends

from tasks.repositories import TaskRepositoryInterface
from tasks.repositories.task_repository_mongo import TaskRepositoryMongo
from tasks.repositories.task_repository_sql import TaskRepositorySql
from tasks.schemas import TaskOut, TaskCreate, TaskUpdate

# Creación del router de FastAPI
router = APIRouter(
    tags=["Task"]
)


# Selección del repositorio
def get_task_repository() -> TaskRepositoryInterface:
    use_mongo: bool = False
    if use_mongo:
        return TaskRepositoryMongo()
    return TaskRepositorySql()


@router.get("/task/{task_id}", response_model=TaskOut)
def read_task(task_id: str, repo: TaskRepositoryInterface = Depends(get_task_repository)):
    task = repo.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


@router.get("/tasks", response_model=List[TaskOut])
def read_tasks(repo: TaskRepositoryInterface = Depends(get_task_repository)):
    return repo.get_tasks()


@router.post("/task", response_model=TaskOut)
def create_task(task: TaskCreate, repo: TaskRepositoryInterface = Depends(get_task_repository)):
    return repo.create_task(task)


@router.put("/task/{task_id}", response_model=TaskOut)
def update_task(task_id: str, task: TaskUpdate, repo: TaskRepositoryInterface = Depends(get_task_repository)):
    return repo.update_task(task_id, task)


@router.delete("/task/{task_id}", response_model=TaskOut)
def delete_task(task_id: str, repo: TaskRepositoryInterface = Depends(get_task_repository)):
    return repo.delete_task(task_id)
