from flask import Blueprint, request
from flask_login import login_required
from flask import current_app as APP

TASK_BP = Blueprint("task", __name__)

@TASK_BP.route("/api/tasks", methods=["POST"])
@login_required
def create_task():
    return APP.task_controller.create_task(request)
    

@TASK_BP.route("/api/tasks")
@login_required
def get_all_tasks():
    return APP.task_controller.get_all_tasks(request)


@TASK_BP.route('/api/tasks/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    return APP.task_controller.get_task(task_id, request)


@TASK_BP.route("/api/tasks/<int:task_id>", methods=['PATCH', 'PUT'])
def update_task(task_id):
    return APP.task_controller.update_task(task_id, request)


@TASK_BP.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    return APP.task_controller.delete_task(task_id)


@TASK_BP.route("/api/tasks/<int:task_id>/execute", methods=["POST"])
@login_required
def execute_task(task_id):
    return APP.task_controller.execute_task(task_id)

