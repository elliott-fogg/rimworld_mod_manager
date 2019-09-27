# The main file that is run to start the program
import tkinter as tk
from class_data_object import data_object
from class_gui import gui

if __name__ == '__main__':
    root = tk.Tk()
    main_gui = gui(root)
    main_gui.tree.populate_treeview_from_data()
    root.mainloop()
