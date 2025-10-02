import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from models.text_classifier import TextClassifierModel
from models.image_captioner import ImageCaptionerModel
from oop.decorators import log_method_calls

class MainApplication:
    """
    This is the main GUI class that implements the Tkinter interface.
    """
    
    def __init__(self, root):
        """
   
        """
        self._root = root
        self._root.title("AI Model Integration GUI - HIT137 Assignment 3")
        self._root.geometry("900x700")
        
        self._text_model = TextClassifierModel()
        self._image_model = ImageCaptionerModel()
        
        self._setup_gui()
    
    def _setup_gui(self):
        """
        It sets the main GUI layout.
      
        """
        self._notebook = ttk.Notebook(self._root)
        self._notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._create_model_processing_tab()
        self._create_oop_explanation_tab()
        self._create_model_info_tab()
    
    def _create_model_processing_tab(self):
        """
        It creates the tab for processing both text and image models.
        """
        main_frame = ttk.Frame(self._notebook)
        self._notebook.add(main_frame, text="AI Model Processing")
        
    
        header_label = ttk.Label(main_frame, text="AI Model Integration System", 
                                font=('Arial', 16, 'bold'))
        header_label.pack(pady=10)
        
  
        selection_frame = ttk.LabelFrame(main_frame, text="Select Model Type")
        selection_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(selection_frame, text="Choose Model:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10, pady=10)
        
        self._model_type_var = tk.StringVar()
        model_dropdown = ttk.Combobox(selection_frame, 
                                     textvariable=self._model_type_var,
                                     values=["Text Classification (Sentiment Analysis)", 
                                            "Image Captioning"],
                                     state="readonly",
                                     width=40)
        model_dropdown.pack(side=tk.LEFT, padx=10, pady=10)
        model_dropdown.current(0)  
        model_dropdown.bind("<<ComboboxSelected>>", self._on_model_change)
        

        self._input_frame = ttk.LabelFrame(main_frame, text="Input")
        self._input_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self._input_container = ttk.Frame(self._input_frame)
        self._input_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self._process_button = ttk.Button(button_frame, text="Process Input", 
                                         command=self._process_input,
                                         style='Accent.TButton')
        self._process_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Clear Output", 
                                 command=self._clear_output)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        output_frame = ttk.LabelFrame(main_frame, text="Output")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        output_scroll = ttk.Scrollbar(output_frame)
        output_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._output_text = tk.Text(output_frame, height=12, width=80, 
                                   yscrollcommand=output_scroll.set,
                                   font=('Courier', 10))
        self._output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        output_scroll.config(command=self._output_text.yview)
        
        self._status_var = tk.StringVar()
        self._status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self._status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)
        
        self._show_text_input()
    
    def _on_model_change(self, event=None):
        """
       It updated the input section based on selected model type.
        """
        selected_model = self._model_type_var.get()
        
        for widget in self._input_container.winfo_children():
            widget.destroy()
        
        if "Text Classification" in selected_model:
            self._show_text_input()
            self._process_button.config(text="Analyze Sentiment")
        elif "Image Captioning" in selected_model:
            self._show_image_input()
            self._process_button.config(text="Generate Caption")
        
        self._clear_output()
        self._status_var.set(f"Selected: {selected_model}")
    
    def _show_text_input(self):
        """
        Displays input widgets for text classification.
        """
        ttk.Label(self._input_container, text="Enter text to analyze:", 
                 font=('Arial', 10)).pack(anchor=tk.W, pady=5)
        
        self._text_input = tk.Text(self._input_container, height=6, width=80,
                                  font=('Arial', 10))
        self._text_input.pack(pady=5, fill=tk.BOTH, expand=True)
        
        placeholder = "Type or paste your text here for sentiment analysis..."
        self._text_input.insert("1.0", placeholder)
        self._text_input.bind("<FocusIn>", lambda e: self._clear_placeholder(self._text_input, placeholder))
    
    def _show_image_input(self):
       
        ttk.Label(self._input_container, text="Select an image file:", 
                 font=('Arial', 10)).pack(anchor=tk.W, pady=5)
        
        file_frame = ttk.Frame(self._input_container)
        file_frame.pack(fill=tk.X, pady=5)
        
        self._image_path_var = tk.StringVar()
        path_entry = ttk.Entry(file_frame, textvariable=self._image_path_var, 
                              width=60, font=('Arial', 10))
        path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(file_frame, text="Browse...", 
                                  command=self._browse_image)
        browse_button.pack(side=tk.LEFT, padx=5)
        
        info_label = ttk.Label(self._input_container, 
                              text="Supported formats: JPG, JPEG, PNG, BMP, GIF",
                              font=('Arial', 9, 'italic'),
                              foreground='gray')
        info_label.pack(anchor=tk.W, pady=5)
    
    def _clear_placeholder(self, text_widget, placeholder):
        
        if text_widget.get("1.0", tk.END).strip() == placeholder:
            text_widget.delete("1.0", tk.END)
    
    @log_method_calls
    def _process_input(self):
        """
       It processes the input based on selected model type.
        """
        selected_model = self._model_type_var.get()
        
        self._status_var.set("Processing...")
        self._root.update()
        
        try:
            if "Text Classification" in selected_model:
                self._process_text()
            elif "Image Captioning" in selected_model:
                self._process_image()
        except Exception as e:
            self._output_text.delete("1.0", tk.END)
            self._output_text.insert(tk.END, f"Error: {str(e)}")
            self._status_var.set("Error occurred")
    
    def _process_text(self):
        """
        It processes text input using the text classification model.
        """
        input_text = self._text_input.get("1.0", tk.END).strip()
        
        if not input_text or input_text == "Type or paste your text here for sentiment analysis...":
            messagebox.showwarning("Warning", "Please enter some text to analyze.")
            self._status_var.set("Ready")
            return
        
        result = self._text_model.process_input(input_text)
        
        self._output_text.delete("1.0", tk.END)
        
        if "error" in result:
            self._output_text.insert(tk.END, f"❌ Error: {result['error']}\n")
            self._status_var.set("Error")
        else:
            output = "=" * 60 + "\n"
            output += "TEXT SENTIMENT ANALYSIS RESULTS\n"
            output += "=" * 60 + "\n\n"
            output += f"Input Text:\n{result['text']}\n\n"
            output += f"Sentiment: {result['sentiment']}\n"
            output += f"Confidence Score: {result['confidence']:.4f} ({result['confidence']*100:.2f}%)\n"
            output += "\n" + "=" * 60 + "\n"
            
            self._output_text.insert(tk.END, output)
            self._status_var.set("Processing complete")
    
    @log_method_calls
    def _browse_image(self):
      
        file_path = filedialog.askopenfilename(
            title="Select an image file",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self._image_path_var.set(file_path)
            self._status_var.set(f"Selected: {file_path.split('/')[-1]}")
    
    def _process_image(self):
       
        image_path = self._image_path_var.get()
        
        if not image_path:
            messagebox.showwarning("Warning", "Please select an image file.")
            self._status_var.set("Ready")
            return
        
        result = self._image_model.process_input(image_path)
        
        self._output_text.delete("1.0", tk.END)
        
        if "error" in result:
            self._output_text.insert(tk.END, f"❌ Error: {result['error']}\n")
            self._status_var.set("Error")
        else:
            output = "=" * 60 + "\n"
            output += "IMAGE CAPTIONING RESULTS\n"
            output += "=" * 60 + "\n\n"
            output += f"Image File: {result['image_path'].split('/')[-1]}\n"
            output += f"Full Path: {result['image_path']}\n\n"
            output += f"Generated Caption:\n\"{result['caption']}\"\n"
            output += "\n" + "=" * 60 + "\n"
            
            self._output_text.insert(tk.END, output)
            self._status_var.set("Processing complete")
    
    def _clear_output(self):
        """
        It clears the output text area.
        """
        self._output_text.delete("1.0", tk.END)
        self._status_var.set("Output cleared")
    
    def _create_oop_explanation_tab(self):
       
        oop_frame = ttk.Frame(self._notebook)
        self._notebook.add(oop_frame, text="OOP Concepts Explanation")
        
      
        title_label = ttk.Label(oop_frame, 
                               text="Object-Oriented Programming Concepts Used",
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
 
        scroll = ttk.Scrollbar(oop_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        explanation_text = """
1. MULTIPLE INHERITANCE

WHERE USED:
 There is a parent inheritance between TextClassifierModel and ImageCaptionerModel classes. 
 classes: LoggingMixin, PerformanceMixin and BaseModel.
 Arguments: class TextClassifierModel( LoggingMixin, PerformanceMixin, BaseModel )

WHY USED:
 Makes it possible to unite functionality of multiple sources without the duplication of codes.
 LoggingMixin offers logging facilities.
 PerformanceMixin introduces the performance tracking (number of calls, time)
 BaseModel offers the framework of all AI models.
 Facilitates reuse and component design - mixins introduce particular functionality.

BENEFIT:
 It avoids the repeating of the same code in different classes
 It makes the code more maintainable and extendable


2. MULTIPLE DECORATORS

WHERE USED:
@execution_timer: Applied the process_input() methods to measure tne execution time
 @validate_input_type: Applied tbe process_input() to validate the input's data types
 @log_method_calls: Applied the GUI methods for tracking methods calls 

WHY USED:
 Decorators does not change the logic in the core method and instead provides the functionality.
 It is based on the principle of Open/Closed that is open to extension and closed to modifications.
 the execution timer is used to measure the time model takes to process input.
 The input validation eliminates the wrong types of data.
 The method call tracing is useful to debug and trace. 

BENEFIT:
 It purges the separation of concerns timing, validation and logging are different. 
  business logic
One can easily add or remove the functionality by merely adding/removing decorator.

3. ENCAPSULATION

WHERE USED:
Private attributes: classifier, model, processor, isloaded, textinput.  
The components of all the internal model are preceded with underscore ().  
The GUI elements are held in the form of a private attribute (root, notebook, outputtext).

WHY USED:
 Hides the internal implementation details from the external access.
 Prevents unintentional modification of important parts of the model.
 It provides the controlled access via public methods, getmodelinfo and process_input.
 Protects the integrity of the internal state of the object.

BENEFIT:
 Increases security and protection of data.
 Increases code maintainability, ensuring that changes made inside the code cannot affect code that sits on the outside.
 Reduces cross coupling between classes.

4. POLYMORPHISM

WHERE USED:
The method process_input() is implemented differently in every model class:
  - TextClassifierModel.process_input(text) → It returns the sentiment analysis
  - ImageCaptionerModel.process_input(image_path) → It returns icaption of the image
 
WHY USED:
It allows the different model types to be used interchangeably
 The same method name (process_input) producesnthe different behaviors based on its object type
 The GUI can call process_input() without know its specific model type
 It enables "duck typing" if it has process_input(),then it can be used as a model

BENEFIT:
 It makes the code more flexible and extendable
 it is easy to add new model types without changing existing code
 This simplifies the GUI logic 


5. METHOD OVERRIDING

WHERE USED:
 The method process_input() that is in TextClassifierModel and ImageCaptionerModel overrides 
  the abstract method from BaseModel
 The method get_model_info() is overridden in each model class to provide specific 
  information about the model

WHY USED:
 Each model type needs its own implementation to process the logic
 BaseModel defines the interface which method to implement
Child classes provide the actual implementation that tells how the model work for it

BENEFIT:
The system enforces a contract which all models must implement the required methods.
It gives flexibility to each model to process input in their own fashion.
It provides for consistency across types of models.

"""
        
        explanation_area = tk.Text(oop_frame, wrap=tk.WORD, width=100, height=35,
                                  font=('Courier', 10),
                                  yscrollcommand=scroll.set)
        explanation_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        explanation_area.insert(tk.END, explanation_text)
        explanation_area.config(state=tk.DISABLED)  # Make read-only
        scroll.config(command=explanation_area.yview)
    
    def _create_model_info_tab(self):
        """
        It creates the tab to display the information about the AI models used.
        
        """
        info_frame = ttk.Frame(self._notebook)
        self._notebook.add(info_frame, text="AI Model Information")
        
       
        title_label = ttk.Label(info_frame, 
                               text="Hugging Face AI Models Information",
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
    
        scroll = ttk.Scrollbar(info_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
       
        info_text = tk.Text(info_frame, wrap=tk.WORD, width=100, height=30,
                           font=('Arial', 10),
                           yscrollcommand=scroll.set)
        info_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        scroll.config(command=info_text.yview)
   
        text_model_info = self._text_model.get_model_info()
        image_model_info = self._image_model.get_model_info()
        
       
        info_content = """
MODEL 1: TEXT CLASSIFICATION (SENTIMENT ANALYSIS)

Model Name:
    {text_name}

Description:
    {text_desc}

Task Category:
    {text_task}

Library:
    {text_lib}

Input Type:
    {text_input}

Output Type:
    {text_output}

About this Model:
    This is a fine-tuned version of DistilBERT, which is a smaller, faster version of 
    BERT (Bidirectional Encoder Representations from Transformers). It has been 
    specifically trained on the SST-2 (Stanford Sentiment Treebank) dataset for 
    binary sentiment classification.
    
   The model classifies all inputs as one of the two sentiment classes, either POSITIVE or
   NEGATIVE and measures the classification by a confidence score.

Model Size:
    ~268 MB (compact and efficient)

Performance:
    Accuracy: ~91% on SST-2 test set


MODEL 2: IMAGE CAPTIONING

Model Name:
    {image_name}

Description:
    {image_desc}

Task Category:
    {image_task}

Library:
    {image_lib}

Input Type:
    {image_input}

Output Type:
    {image_output}

About this Model:
BLIP (Bootstrapping LanguageImage Pre-Training) is a state-of-the-art vision-language model that was 
developed by Salesforce Research. It can provide natural-language descriptions of pictures through a
combination of knowledge of both visual features and linguistic context.
This model makes use of a vision transformer to manipulate images and a language model in order to generate descriptive captions. Applications used include:
* Image description to be automated in order to be accessable.
* Optimization of content and search engine optimization.
* Creation of social-media-content.
* Visual storytelling
Model Size:
    ~990 MB (base version)

Performance:
    Achieves competitive scores on COCO and other captioning benchmarks


WHY THESE MODELS WERE SELECTED

1. Different Categories:
   • Text Classification (NLP) vs Image Captioning (Computer Vision)
   • Demonstrates versatility across multiple AI domains

2. Free and Accessible:
   • Hugging Face has both models freely available
   • API-free and authentication-free.
   • Directly compatible with the Transformers library.

3. Reasonable Size:
   • * Small enough that it can be downloaded and executed on standard equipment.
 Can be loaded and operated in real time application.

""".format(
            text_name=text_model_info['name'],
            text_desc=text_model_info['description'],
            text_task=text_model_info['task'],
            text_lib=text_model_info['library'],
            text_input=text_model_info['input_type'],
            text_output=text_model_info['output_type'],
            image_name=image_model_info['name'],
            image_desc=image_model_info['description'],
            image_task=image_model_info['task'],
            image_lib=image_model_info['library'],
            image_input=image_model_info['input_type'],
            image_output=image_model_info['output_type']
        )
        
        info_text.insert(tk.END, info_content)
        info_text.config(state=tk.DISABLED)  # Make read-only


def main():
    """
    This is the entry point of the application.
    """
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()