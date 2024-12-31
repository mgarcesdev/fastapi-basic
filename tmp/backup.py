from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# Puerto del Servicio
PORT = 8001

# Configuración de la conexión a SQLite
DATABASE_URL = "sqlite:///./task_database.db"
#DATABASE_URL = "postgresql://postgres:my_secure_password@localhost:5432/my_database"

# Configuración de SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Modelo de tabla para SQLAlchemy
class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# Modelos Pydantic (desacoplados completamente de la base de datos)
class TaskOut(BaseModel):
    id: str  # Usamos str para que funcione tanto con Mongo como con SQL
    description: str
    is_completed: bool
    created_at: datetime


class TaskCreate(BaseModel):
    description: str


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    is_completed: Optional[bool] = None


# Interfaz común para los repositorios
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


# Implementación del repositorio para SQL
class TaskRepositorySql(TaskRepositoryInterface):
    def __init__(self):
        self.db = SessionLocal()

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


# Implementación del repositorio para MongoDB
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


# Selección del repositorio
def get_task_repository() -> TaskRepositoryInterface:
    use_mongo: bool = False
    if use_mongo:
        return TaskRepositoryMongo()
    return TaskRepositorySql()


# Endpoints de la API
app = FastAPI()


@app.get("/task/{task_id}", response_model=TaskOut)
def read_task(task_id: str, repo: TaskRepositoryInterface = Depends(get_task_repository)):
    task = repo.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


@app.get("/tasks", response_model=List[TaskOut])
def read_tasks(repo: TaskRepositoryInterface = Depends(get_task_repository)):
    return repo.get_tasks()


@app.post("/task", response_model=TaskOut)
def create_task(task: TaskCreate, repo: TaskRepositoryInterface = Depends(get_task_repository)):
    return repo.create_task(task)


@app.put("/task/{task_id}", response_model=TaskOut)
def update_task(task_id: str, task: TaskUpdate, repo: TaskRepositoryInterface = Depends(get_task_repository)):
    return repo.update_task(task_id, task)


@app.delete("/task/{task_id}", response_model=TaskOut)
def delete_task(task_id: str, repo: TaskRepositoryInterface = Depends(get_task_repository)):
    return repo.delete_task(task_id)


def run_server():
    Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT, reload=False)


run_server()