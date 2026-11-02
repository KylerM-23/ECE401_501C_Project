import tkinter as tk

root = None

def main():
    root = tk.Tk()

    # Configure the window settings
    root.title("Your Music Wrapped")
    root.geometry("800x800")  # Width x Height in pixels
    root.configure(bg="#f0f0f0")  # Background color


    GuiFunc.rainbow_bg()
    root.mainloop()