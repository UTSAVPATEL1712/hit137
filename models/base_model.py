

from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    This is the abstract base class for AI models.
    """
    
    def __init__(self, model_name, model_description):
        """
        It initializes the base model with name and description.
          """
        super().__init__() 
        self._model_name = model_name  
        self._model_description = model_description  
        self._is_loaded = False  
    
    @property
    def model_name(self):
        """
        This is the getter for the model name attribute.
        """
        return self._model_name
    
    @property
    def model_description(self):
        """
        This is the gertter for the model description attribute.
    
        """
        return self._model_description
    
    @property
    def is_loaded(self):
        """
        This is the getter for the model loading status.
       
        """
        return self._is_loaded
    
    @abstractmethod
    def load_model(self):
        """
        Abstract method which has to be implemented by sub classes to load the model.
       
        """
        pass
    
    @abstractmethod
    def process_input(self, input_data):
        """
        Abstract method that should be implemented by subclasses to process the input.
        
        """
        pass