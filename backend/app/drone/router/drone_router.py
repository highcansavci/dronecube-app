from flask import Blueprint, request
from flask_login import login_required
from flask import current_app as APP

DRONE_BP = Blueprint("drone", __name__)

@DRONE_BP.route("/api/drones")
@login_required
def get_all_drones():
    return APP.drone_controller.get_all_drones(request)

@DRONE_BP.route("/api/drones/filter", methods=["POST"])
@login_required
def filter_all_drones():
    return APP.drone_controller.filter_all_drones(request)        

@DRONE_BP.route("/api/drones", methods=["POST"])
@login_required
def create_drone():
    return APP.drone_controller.create_drone(request)

@DRONE_BP.route('/api/drones/<int:drone_id>', methods=['GET'])
@login_required
def get_drone(drone_id):
    return APP.drone_controller.get_drone(drone_id)

@DRONE_BP.route("/api/drones/<int:drone_id>", methods=['PATCH', 'PUT'])
@login_required
def update_drone(drone_id):
    return APP.drone_controller.update_drone(drone_id, request)

@DRONE_BP.route("/api/drones/<int:drone_id>", methods=["DELETE"])
@login_required
def delete_drone(drone_id):
    return APP.drone_controller.delete_drone(drone_id)

@DRONE_BP.route("/api/drones/<int:drone_id>/tasks/<int:task_id>/assign")
@login_required
def assign_task_to_drone(drone_id, task_id):
    return APP.drone_controller.assign_task_to_drone(drone_id, task_id)

@DRONE_BP.route("/api/drones/<int:drone_id>/tasks/<int:task_id>/execute")
@login_required
def start_executing_task(drone_id, task_id):
    return APP.drone_controller.start_executing_task(drone_id, task_id)

@DRONE_BP.route("/api/drones/<int:drone_id>/tasks/<int:task_id>/cancel_execution")
@login_required
def cancel_task_execution(drone_id, task_id):
    return APP.drone_controller.cancel_task_execution(drone_id, task_id)

@DRONE_BP.route("/api/drones/<int:drone_id>/tasks/<int:task_id>/cancel_assignment")
@login_required
def cancel_task_assignment(drone_id, task_id):
    return APP.drone_controller.cancel_task_assignment(drone_id, task_id)

@DRONE_BP.route("/api/drones/<int:drone_id>/tasks/bulk_assign", methods=["POST"])
@login_required
def bulk_assign_tasks_to_drone(drone_id):
    return APP.drone_controller.bulk_assign_tasks_to_drone(drone_id, request)

@DRONE_BP.route("/api/drones/<int:drone_id>/tasks/bulk_execute", methods=["POST"])
@login_required
def bulk_add_tasks_to_execution(drone_id):
    return APP.drone_controller.bulk_add_tasks_to_execution(drone_id, request)

@DRONE_BP.route("/api/drones/<int:drone_id>/tasks/bulk_cancel_execution", methods=["POST"])
@login_required
def bulk_cancel_task_execution(drone_id):
    return APP.drone_controller.bulk_cancel_task_execution(drone_id, request)

@DRONE_BP.route("/api/drones/<int:drone_id>/tasks/bulk_cancel_assignment", methods=["POST"])
@login_required
def bulk_cancel_task_assignment(drone_id):
    return APP.drone_controller.bulk_cancel_task_assignment(drone_id, request)
