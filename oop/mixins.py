
class LoggingMixin:
    """
    A mixin class that provides logging functionality to other classes.
    This mixin is designed to be used with model classes to add logging capabilities without inheritance from a base class.
    """
    
    def log_info(self, message):
        """
        Logs the messages onto the console.
        This method is used by the classes that inherit from this class.
        
        """
        print(f"[INFO] {message}")
    
    def log_error(self, message):
        """
        Logs the error message onto the console.
        This method is used by the classes that inherit from this class.
        """
        print(f"[ERROR] {message}")

class PerformanceMixin:
    """
    The class also offers performance monitoring.
    The classes which inherit this class use this method.

    """
    
    def __init__(self, *args, **kwargs):
      
        super().__init__(*args, **kwargs)
        self._call_count = 0 
    
    def track_call(self):
        """
        Increments the call count to monitor the number of times a method has been called.
        """
        self._call_count += 1
    
    def get_call_count(self):
        """
        It returns the number of times this method have been called.
        """
        return self._call_count