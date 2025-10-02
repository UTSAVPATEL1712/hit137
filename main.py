import tkinter as tk
from gui.main_window import MainApplication

def main():
    """
    This is the main entry point for the application.
    """
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()