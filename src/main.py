import uvicorn
from fastapi import FastAPI

from config import Config
from dependencies import initialize_dependencies
from tasks import setup_route


def run_server():
    # Puerto del Servicio
    config = Config()

    # Inicializamos la app
    app = FastAPI(
        title="Tasks API",
        description="API para gestionar tareas",
        version=config.VERSION,
        docs_url="/",
    )

    dependencies = initialize_dependencies(config)
    tasks_router = setup_route(dependencies["task_controller"])
    app.include_router(tasks_router)

    uvicorn.run(app, host="0.0.0.0", port=config.PORT, reload=config.DEBUG)


if __name__ == "__main__":
    run_server()
