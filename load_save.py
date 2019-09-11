import os, re, glob
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import ttk

folder = {}
folder["steam mods"] = "C:/Program Files (x86)/Steam/steamapps/workshop/content/294100"
folder["rimworld mods"] = "C:/Program Files (x86)/Steam/steamapps/common/RimWorld/Mods"
folder["modconfig"] = "C:/Users/Foggy/AppData/LocalLow/Ludeon Studios/RimWorld by Ludeon Studios/Config/ModsConfig.xml"
# Locate default mod folder
# Locate default rimwold/mods folder
# Locate default config/modsconfig file
# Load everything into memory
# Load the latest user name
# Load the latest user info
# Load saved list of mod information (just the IDs)
# Compare to the latest mod info
# Save list of mod information

def get_folder():
    root = tk.Tk()
    root.withdraw()
    root.update()
    folder = fd.askdirectory()
    root.update()
    root.destroy()
    return folder

def locate_steam_mod_folder():
    if os.path.isdir(folder["steam mods"]):
        return folder["steam mods"]
    else:
        new_path = get_folder()
        if len(new_path) > 0:
            return new_path
        else:
            return None

def load_mod_info(mod_path):
    mod_list = os.listdir(mod_path)
    mod_array = {}
    for mod_num in mod_list:
        if not os.path.isdir("{}/{}/About".format(mod_path,mod_num)):
            continue
        about = open("{}/{}/About/About.xml".format(mod_path,mod_num),encoding="latin-1")
        about_contents = about.read()
        mod_title = re.findall("<name>(.+?)</name>",about_contents)[0]
        mod_author = re.findall("<author>(.+?)</author>",about_contents)[0]
        mod_version ="0.19" #re.findall("<target[Vv]ersion>(.+?)</target[Vv]ersion>",about_contents)[0]
        try:
            mod_url = re.findall("<url>(.+)</url>",about_contents)[0]
        except:
            mod_url = ""
        try:
            mod_description = re.findall("<description>((?:.|\s)+?)</description>",about_contents)[0]
        except:
            mod_description = ""

        mod_array[mod_num] = {}
        mod_array[mod_num]["title"] = mod_title
        mod_array[mod_num]["author"] = mod_author
        mod_array[mod_num]["version"] = mod_version
        mod_array[mod_num]["description"] = mod_description
        mod_array[mod_num]["url"] = mod_url

    return mod_array

def load_user_info():
    # Open the file
    # Load the list of categories
    # Load the list of files, in the manner:
    ## file_id, activated_true/false, category_number
    pass

root = tk.Tk()

vsb = ttk.Scrollbar(orient="vertical")
hsb = ttk.Scrollbar(orient="horizontal")

tree = ttk.Treeview(columns=("mod","author","version","url"),
    displaycolumns=("author","version","url"),
    yscrollcommand=vsb.set,
    xscrollcommand=hsb.set
    )

vsb['command'] = tree.yview
hsb['command'] = tree.xview

tree.heading("#0", text="Title", anchor='w')
tree.heading("author", text="Author", anchor="w")
tree.heading("version", text="Version", anchor="w")
tree.heading("url", text="URL", anchor="w")
tree.column("author", stretch=0, width=100)
tree.column("version", stretch=0, width=100)
tree.column("url", stretch=0, width=100)

categories = ("Medieval,Spacer,Cosmetic,QoL,Unsorted")
categories = categories.split(",")
for c in categories:
    id = tree.insert("","end",c,text=c)
mod_info = load_mod_info(folder["steam mods"])
print(mod_info['975316762'])
mod_ids = sorted(mod_info.keys(),reverse=False,key=lambda x: mod_info[x]["title"].lower())
for _id in mod_ids:
    vnum = mod_info[_id]["version"]
    if float(vnum[2:]) < 18:
        tag = "outdated"
    else:
        tag = "indate"
    id = tree.insert("Unsorted","end",_id,text=mod_info[_id]["title"],tags=(tag,))
    tree.set(id,"author",mod_info[_id]["author"])
    tree.set(id,"version",mod_info[_id]["version"])
    tree.set(id,"url",mod_info[_id]["url"])

tree.insert('', 'end', 'widgets', text='Widget Tour')
tree.tag_configure('outdated', background='orange')

# Arrange the tree and its scrollbars in the toplevel
tree.grid(column=0, row=0, sticky='nswe')
vsb.grid(column=1, row=0, sticky='ns')
hsb.grid(column=0, row=1, sticky='ew')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
