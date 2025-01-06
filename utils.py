from tkinter import ttk

def apply_styles():
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 12))
    style.configure("TCombobox", font=("Helvetica", 12))
    style.configure("TProgressbar", thickness=20)
    
    # Add a style for the result label
    style.configure("Result.TLabel", font=("Helvetica", 14), foreground="Green")#background="yellow")
