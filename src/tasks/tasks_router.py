from fastapi import APIRouter

from tasks.controller.task_controller import TaskController


def setup_route(task_controller: TaskController):
    router = APIRouter(tags=["Task"])

    router.add_api_route("/task/{task_id}", task_controller.read_task, methods=["GET"])
    router.add_api_route("/tasks", task_controller.read_tasks, methods=["GET"])
    router.add_api_route("/task", task_controller.create_task, methods=["POST"])
    router.add_api_route("/task/{task_id}", task_controller.update_task, methods=["PUT"])
    router.add_api_route("/task/{task_id}", task_controller.delete_task, methods=["DELETE"])
    return router
