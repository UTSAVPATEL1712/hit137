# oop/mixins.py

class LoggingMixin:
    """
    A mixin class that provides logging functionality to other classes.
    This mixin is designed to be used with model classes to add logging capabilities without inheritance from a base class.
    """
    
    def log_info(self, message):
        """
        Logs an informational message to the console.
        This method is used by classes that inherit from this mixin to provide status updates.
        """
        print(f"[INFO] {message}")
    
    def log_error(self, message):
        """
        Logs an error message to the console.
        This method is used by classes that inherit from this mixin to report errors.
        """
        print(f"[ERROR] {message}")

class PerformanceMixin:
    """
    A mixin class that provides performance tracking capabilities.
    This mixin is intended to be used with model classes to track their performance metrics.
    It uses super() to ensure the initialization chain continues correctly,
    passing along any arguments it doesn't use.
    """
    
    def __init__(self, *args, **kwargs):
        # Call the next constructor in the MRO, passing along all arguments
        # This allows classes like BaseModel (which requires specific args) to receive them.
        super().__init__(*args, **kwargs)
        self._call_count = 0 # Initialize the call counter attribute
    
    def track_call(self):
        """
        Increments the call counter to track how many times a method has been invoked.
        This method is used to monitor the usage of model inference methods.
        """
        self._call_count += 1
    
    def get_call_count(self):
        """
        Returns the number of times tracking methods have been called.
        This method provides access to the internal call counter for performance analysis.
        """
        return self._call_count