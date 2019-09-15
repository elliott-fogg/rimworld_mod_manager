# A class page from which to construct various Frames. All template classes
# should be contained here, and accessed by each Frame script as needed.

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

class page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.position()

    def show(self):
        self.lift()

    def position(self):
        pass
