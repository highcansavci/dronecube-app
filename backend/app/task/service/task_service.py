class TaskService:
    def get_current_user(self):
        raise NotImplementedError
    
    def query_drone(self, drone_id):
        raise NotImplementedError
    
    def serialize_task(self, task):
        raise NotImplementedError
    
    def serialize_all_tasks(self, tasks):
        raise NotImplementedError
    
    def create_task(self, data):
        raise NotImplementedError
    
    def get_all_tasks(self):
        raise NotImplementedError
    
    def get_task(self, task_id):
        raise NotImplementedError
    
    def update_task(self, data, task):
        raise NotImplementedError
    
    def delete_task(self, task):
        raise NotImplementedError
    
    def execute_task(self, task, task_id):
        raise NotImplementedError
    
    def save_image(self, filename, task_id):
        raise NotImplementedError
    
    def complete_task(self, task):
        raise NotImplementedError
    