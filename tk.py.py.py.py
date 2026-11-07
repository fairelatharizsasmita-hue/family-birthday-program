import tkinter as tk
from tkinter import Tk, Canvas
root = tk.Tk()
label = tk.Label(root, text="Hello, Tkinter!")
label.pack()
canvas = Canvas(root, width=1240, height=1240, bg="white")
canvas.pack()
root.mainloop()