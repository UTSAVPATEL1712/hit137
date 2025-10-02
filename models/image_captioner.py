

from .base_model import BaseModel
from oop.mixins import LoggingMixin, PerformanceMixin
from oop.decorators import execution_timer, validate_input_type
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch


class ImageCaptionerModel(LoggingMixin, PerformanceMixin, BaseModel):
    """
    This class inherits from BaseModel and uses its multiple methods.
    """
    
    def __init__(self):
        """
        Initializing the image caption model with its name and description.
        
        """
        super().__init__(
           
        )
        self._processor = None
        self._model = None
    

    def load_model(self):
        """
        This method loads the image captioning model.
        """
        try:
            self.log_info(f"Loading model: {self._model_name}")
            self._processor = BlipProcessor.from_pretrained(self._model_name)
            self._model = BlipForConditionalGeneration.from_pretrained(self._model_name)
            self._is_loaded = True
            self.log_info("Image captioning model loaded successfully")
        except Exception as e:
            self.log_error(f"Failed to load image captioning model: {str(e)}")
            self._is_loaded = False
    
    @execution_timer
    @validate_input_type(str)  # Validates file path
    def process_input(self, image_path):
        """
        It process the input image and returns a caption.
       
        """
        if not self._is_loaded:
            self.load_model()
        
        self.track_call()
        
        try:
           
            raw_image = Image.open(image_path).convert('RGB')
            
           
            inputs = self._processor(raw_image, return_tensors="pt")
            out = self._model.generate(**inputs)
            caption = self._processor.decode(out[0], skip_special_tokens=True)
            
            return {
                "image_path": image_path,
                "caption": caption
            }
        except Exception as e:
            self.log_error(f"Error processing image input: {str(e)}")
            return {"error": f"Processing failed: {str(e)}"}
    
    def get_model_info(self):
       
        return {
            "name": self._model_name,
            "description": self._model_description,
            "task": "Image Captioning",
            "library": "Transformers",
            "input_type": "Image file path",
            "output_type": "Text caption describing the image"
        }
