from sqlalchemy import create_engine

from config import Config
from tasks.controller.task_controller import TaskController
from tasks.repositories.task_repository_sql import TaskRepositorySql


def initialize_dependencies(config: Config):
    # Crear el engine de la base de datos
    engine = create_engine(config.DATABASE_URL)

    # Inicializar las dependencias del repositorio, servicio y controlador
    task_repository = TaskRepositorySql(engine)
    # task_service = TaskService(task_repository)
    task_controller = TaskController(task_repository)

    return {
        "task_repository": task_repository,
        "task_controller": task_controller,
    }
