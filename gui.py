import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from load_mod_information import data_object

UNSORTED = "Unsorted"

class gui(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.img = ImageTk.PhotoImage(Image.open("preview.png"))

        self.position()

    def position(self):
        self.f1 = tk.Frame(self)
        self.f2 = tk.Frame(self)
        self.f3 = tk.Frame(self)

        self.f1.grid(row=0)
        self.f2.grid(row=1)
        self.f3.grid(row=2)

        self.button_temp1 = tk.Button(master=self.f1, text="PLACEHOLDER")
        self.button_temp1.grid(row=0, sticky=tk.W)

        self.tree = treeview(master=self.f2)
        self.tree.pack()

        self.button_temp2 = tk.Button(master=self.f3, text="PLACEHOLDER")
        self.button_temp2.pack()

        self.grid(row=0)


class treeview(tk.Frame):
    def __init__(self, master, data=None):
        tk.Frame.__init__(self, master)

        self.vsb = ttk.Scrollbar(orient="vertical")
        self.hsb = ttk.Scrollbar(orient="horizontal")

        tree = ttk.Treeview(master=self,
            columns=("author","version","url","order","id"),
            displaycolumns=("author","version","url","order","id"),
            yscrollcommand=self.vsb.set,
            xscrollcommand=self.hsb.set
            )

        self.tree = tree

        self.vsb['command'] = tree.yview
        self.hsb['command'] = tree.xview

        tree.heading("#0", text="Title", anchor="w")
        tree.heading("author", text="Author", anchor="w")
        tree.heading("version", text="Version", anchor="w")
        tree.heading("url", text="URL", anchor="w")
        tree.heading("order", text="Order", anchor="e")
        tree.column("author", stretch=0, width=100)
        tree.column("version", stretch=0, width=100)
        tree.column("url", stretch=0, width=100)
        tree.column("order", stretch=0, width=100)

        categories = ("Medieval,Spacer,Cosmetic,QoL" + "," + UNSORTED)
        categories = categories.split(",")
        for c in categories:
            id = tree.insert("","end",c,text=c)

        self.add_entry(title="Example_title", author="Example_author", version="1.0", url="example_url", order=3)

        self.tree.grid(column=0, row=0, sticky='nswe')
        self.vsb.grid(column=1, row=0, sticky='ns')
        self.hsb.grid(column=0, row=1, sticky='ew')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def add_entry(self, category=None, title="No Name", author=None,
            version=None, url=None, order=None):
        if category == None:
            category = UNSORTED
        id = self.tree.insert(category, "end", text=title)
        self.tree.set(id, "author", author)
        self.tree.set(id, "version", version)
        self.tree.set(id, "url", url)
        self.tree.set(id, "order", order)

# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate
#     root.destroy()  # this is necessary on Windows to prevent Fatal Python Error: PyEval_RestoreThread: NULL tstate

def main():
    root = tk.Tk()
    data = data_object()
    mod_array = data.mods
    main_gui = gui(root)
    for mod_num in mod_array:
        mod = mod_array[mod_num]
        main_gui.tree.add_entry(title=mod["title"], author=mod["author"],
            version=mod["version"], url=mod["url"])
    root.mainloop()

if __name__=="__main__":
    main()
