from flask import jsonify

class ImageController:
    # Singleton Controller
    _instance = None

    def __init__(self, image_service, task_service) -> None:
        self.image_service = image_service
        self.task_service = task_service
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ImageController, cls).__new__(cls)
            cls._instance.__initialize(*args, **kwargs)
        return cls._instance

    def __initialize(self, image_service, task_service):
        self.image_service = image_service
        self.task_service = task_service  
        
        
    def get_all_images(self, task_id, request):
        task = self.task_service.get_task(task_id)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return self.image_service.serialize_images(task)
        return jsonify({'message': 'Invalid request header'}), 400
    
    def get_image(self, task_id, image_id, request):
        task = self.task_service.get_task(task_id)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            image = self.image_service.get_image(task, image_id)
            filename = image.filename
            url = self.image_service.get_image_url(filename)
            return jsonify({'url': url, 'filename': filename})
        return jsonify({'message': 'Invalid request header'}), 400
    
    
      
    