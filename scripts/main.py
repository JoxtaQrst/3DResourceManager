import tkinter as tk
from gui import create_gui

def main():
    root = tk.Tk()
    root.title("3D Model Utility")
    root.geometry("1250x800")  # Set the window size to 800x600 pixels
    create_gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
