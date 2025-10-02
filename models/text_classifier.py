

from .base_model import BaseModel
from oop.mixins import LoggingMixin, PerformanceMixin
from oop.decorators import execution_timer, validate_input_type
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification


class TextClassifierModel(LoggingMixin, PerformanceMixin, BaseModel):
    """
    This class provides an implementaion of the BaseModel for text classification model.   
    """
    
    def __init__(self):
        """
        This loads the text classifier model with its own name and description.
      
        """
    
        super().__init__(
            "distilbert-base-uncased-finetuned-sst-2-english",
            "Text sentiment classification model using DistilBERT"
        )
        self._classifier = None
        self._tokenizer = None
    
    # ... rest of the class remains the same ...

    def load_model(self):
        """
         This method loads the text classification model from Hugging Face.
        """
        try:
            self.log_info(f"Loading model: {self._model_name}")
            self._classifier = pipeline(
                "sentiment-analysis",
                model=self._model_name,
                tokenizer=self._model_name
            )
            self._is_loaded = True
            self.log_info("Text classification model loaded successfully")
        except Exception as e:
            self.log_error(f"Failed to load text classification model: {str(e)}")
            self._is_loaded = False
    
    @execution_timer
    @validate_input_type(str)
    def process_input(self, input_text):
        """
        It processed the input text and returns analysis results.

        """
        if not self._is_loaded:
            self.load_model()
        
        self.track_call() 
        
        if not input_text.strip():
            return {"error": "Input text cannot be empty"}
        
        try:
            result = self._classifier(input_text)
            return {
                "text": input_text,
                "sentiment": result[0]['label'],
                "confidence": result[0]['score']
            }
        except Exception as e:
            self.log_error(f"Error processing text input: {str(e)}")
            return {"error": f"Processing failed: {str(e)}"}
    
    def get_model_info(self):
       
        return {
            "name": self._model_name,
            "description": self._model_description,
            "task": "Text Sentiment Classification",
            "library": "Transformers",
            "input_type": "Text",
            "output_type": "Sentiment (Positive/Negative) with confidence score"
        }
