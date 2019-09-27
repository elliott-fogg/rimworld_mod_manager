import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from class_data_object import data_object
import webbrowser

UNSORTED = "Unsorted"

def find_item(dd, text):
    try:
        key = next(key for key, value in dd.items() if value == text)
        return key
    except StopIteration:
        return None

class gui(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.data = data_object()
        # self.img = ImageTk.PhotoImage(Image.open("preview.png"))
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

        self.tree = treeview_no_groups(master=self.f2)
        self.tree.pack()

        self.button_temp2 = tk.Button(master=self.f3, text="PLACEHOLDER")
        self.button_temp2.pack()

        self.grid(row=0)


# class treeview(tk.Frame):
#     def __init__(self, master, data=None):
#         tk.Frame.__init__(self, master)
#
#         self.vsb = ttk.Scrollbar(orient="vertical")
#         self.hsb = ttk.Scrollbar(orient="horizontal")
#
#         tree = ttk.Treeview(master=self,
#             columns=("author","version","url","order","id"),
#             displaycolumns=("author","version","url","order","id"),
#             yscrollcommand=self.vsb.set,
#             xscrollcommand=self.hsb.set
#             )
#
#         self.tree = tree
#
#         self.vsb['command'] = tree.yview
#         self.hsb['command'] = tree.xview
#
#         tree.heading("#0", text="Title", anchor="w")
#         tree.heading("author", text="Author", anchor="w")
#         tree.heading("version", text="Version", anchor="w")
#         tree.heading("url", text="URL", anchor="w")
#         tree.heading("order", text="Order", anchor="e")
#         tree.column("author", stretch=0, width=100)
#         tree.column("version", stretch=0, width=100)
#         tree.column("url", stretch=0, width=100)
#         tree.column("order", stretch=0, width=100)
#
#         categories = ("Medieval,Spacer,Cosmetic,QoL" + "," + UNSORTED)
#         categories = categories.split(",")
#         for c in categories:
#             id = tree.insert("","end",c,text=c)
#
#         self.tree.grid(column=0, row=0, sticky='nswe')
#         self.vsb.grid(column=1, row=0, sticky='ns')
#         self.hsb.grid(column=0, row=1, sticky='ew')
#
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(0, weight=1)
#
#         self.test()
#
#     def add_entry(self, category=None, title="No Name", author=None,
#             version=None, url=None, order=None):
#         if category == None:
#             category = UNSORTED
#         id = self.tree.insert(category, "end", text=title)
#         self.tree.set(id, "author", author)
#         self.tree.set(id, "version", version)
#         self.tree.set(id, "url", url)
#         self.tree.set(id, "order", order)
#
#     def test(self):
#         self.add_entry(title="Example Title", author="Example Author",
#             version="Version_Num", url="Example URL", order="Order_Num")

class treeview_no_groups(tk.Frame):
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

        self.tree.grid(column=0, row=0, sticky='nswe')
        self.vsb.grid(column=1, row=0, sticky='ns')
        self.hsb.grid(column=0, row=1, sticky='ew')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tree.bind("<Button-2>", self.middle_click)

    def add_entry(self, title="No Name", author=None,
            version=None, url=None, order=None):
        id = self.tree.insert("", "end", text=title)
        self.tree.set(id, "author", author)
        self.tree.set(id, "version", version)
        self.tree.set(id, "url", url)
        self.tree.set(id, "order", order)

    def populate_treeview_from_data(self):
        for mod_num in master.data.mods:
            mod = data.mods[mod_num]
            self.tree.add_entry(title=mod["title"], author=mod["author"],
                version=mod["version"], url=mod["url"])

    def middle_click(self, event):
        print("Middle button pressed!")
        iid = self.tree.identify_row(event.y)
        if iid:
            # mouse pointer is over an item
            self.tree.selection_set(iid)
            values = self.tree.item(iid)["values"]

            if values[3] == True:
                values[3] = ''
                print("'{}' deactivated".format(self.tree.item(iid)["text"]))
            else:
                values[3] = 1
                print("'{}' activated".format(self.tree.item(iid)["text"]))
            self.tree.item(iid,values=values)
            print(self.tree.item(iid))

            print(self.tree.children)

        else:
            # mouse pointer not over an item, no action required
            pass

    def set_active(self, iid):
        # If not active, set to len(active) + 1
        # If active, set to inactive and relabel all active
        pass

    # def renumber_active(self):

def open_steam_url(): #TEMPORARY
    # webbrowser.open_new(steam_url)
    webbrowser.open_new('steam://url/CommunityFilePage/708455313')

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
    open_steam_url()
    # main()
