import os
from PIL import Image

def validate_image_file(file_path):
    """
    It validates that the provided file path points to a valid image file.
    """
    if not os.path.exists(file_path):
        return False, "File does not exist"
    
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True, "Valid image file"
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"

def format_model_output(result):
    """
    It formats the model output to display on the GUI.
    """
    if "error" in result:
        return f"Error: {result['error']}"
    
    formatted_output = ""
    for key, value in result.items():
        formatted_output += f"{key.title()}: {value}\n"
    
    return formatted_output.strip()