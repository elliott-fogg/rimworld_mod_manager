# The main file that is run to start the program
import tkinter as tk
from load_mod_information import data_object
from gui import gui

if __name__ == '__main__':
    root = tk.Tk()
    data = data_object()
    main_gui = gui(root)
    for mod_num in data.mods:
        mod = data.mods[mod_num]
        main_gui.tree.add_entry(title=mod["title"], author=mod["author"],
            version=mod["version"], url=mod["url"])
    root.mainloop()
