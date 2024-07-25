from builtins import NotImplementedError


class DroneService:
    def get_current_user(self):
        raise NotImplementedError
    
    def serialize_drones(self, drones):
        raise NotImplementedError
    
    def serialize_drone(self, drone):
        raise NotImplementedError
    
    def filter_all_drones(self, drones, form):
        raise NotImplementedError
    
    def create_drone(self, user, name, user_input):
        raise NotImplementedError
    
    def query_drone(self, drone_id):
        raise NotImplementedError
    
    def broadcast_drone_information(self, drone):
        raise NotImplementedError
    
    def update_drone(self, drone, data):
        raise NotImplementedError
    
    def delete_drone(self, drone):
        raise NotImplementedError
    
    def async_connect_drone(self, drone_id):
        raise NotImplementedError
    
    def connect_drone(self, drone):
        raise NotImplementedError
    
    def query_task(self, task_id):
        raise NotImplementedError
    
    def assign_task_to_drone(self, drone, task):
        raise NotImplementedError
    
    def start_executing_task(self, drone, task):
        raise NotImplementedError
    
    def cancel_task_execution(self, drone, task):
        raise NotImplementedError
    
    def cancel_task_assignment(self, drone, task):
        raise NotImplementedError
    
    def bulk_assign_tasks_to_drone(self, drone_id, task_ids):
        raise NotImplementedError

    def bulk_add_tasks_to_execution(self, drone_id, task_ids):
        raise NotImplementedError
    
    def bulk_cancel_task_execution(self, drone_id, task_ids):
        raise NotImplementedError

    def bulk_cancel_task_assignment(self, drone_id, task_ids):
        raise NotImplementedError