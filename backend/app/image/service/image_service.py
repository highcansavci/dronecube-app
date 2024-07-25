class ImageService:
    def serialize_images(self, task):
        raise NotImplementedError
    
    def get_image(self, task, image_id):
        raise NotImplementedError
    
    def get_image_url(self, filename):
        raise NotImplementedError
    
    def save_image(self, filename, task_id):
        raise NotImplementedError