import uvicorn
from fastapi import FastAPI

from config import Config
from tasks import router as tasks_router

# Puerto del Servicio
PORT = 8001

# Inicializamos la app
app = FastAPI(
    title="Tasks API",
    description="API para gestionar tareas",
    version="0.1.0",
    docs_url="/",
)

# Montamos el router con las rutas de tasks
app.include_router(tasks_router)


def run_server():
    config = Config()
    uvicorn.run(app, host="127.0.0.1", port=config.PORT, reload=config.DEBUG)


if __name__ == "__main__":
    run_server()
