from flask import Blueprint, request
from flask_login import login_required
from flask import current_app as APP

IMAGE_BP = Blueprint("image", __name__)

@IMAGE_BP.route("/api/tasks/<int:task_id>/images/view")
@login_required
def get_all_images(task_id):
    return APP.image_controller.get_all_images(task_id, request)


@IMAGE_BP.route("/api/tasks/<int:task_id>/images/view/<int:image_id>")
@login_required
def get_image(task_id, image_id):
    return APP.image_controller.get_image(task_id, image_id, request)

