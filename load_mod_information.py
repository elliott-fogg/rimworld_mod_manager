# Locate mod folder(s)
# Load mod information
# Load mod order
# Locate executable file location
from os.path import join as pjoin
from os.path import isfile, isdir
import os, time, subprocess, re, configparser

# DEFAULTS




class paths():

    default_paths = {
        "root_folder": "C:/Program Files (x86)/Steam/steamapps/common/RimWorld/",
        "executable": "C:/Program Files (x86)/Steam/steamapps/common/RimWorld/RimWorldWin64.exe",
        "mod_folders": ["C:/Program Files (x86)/Steam/steamapps/common/RimWorld/Mods",
            "C:/Program Files (x86)/Steam/steamapps/workshop/content/294100"],
        "mods_config": "~/AppData/LocalLow/Ludeon Studios/Rimworld by Ludeon Studios/Config/ModsConfig.xml",
        "version": "C:/Program Files (x86)/Steam/steamapps/common/RimWorld/Version.txt"
    }

    key_types = {
        "root_folder": "dir",
        "executable": "file",
        "mods_config": "file",
        "version": "file",
        "mod_folders": "multiple_dir"
    }

    def __init__(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        self.location = pjoin(current_dir, "directories.ini")
        if isfile(self.location):
            self.load()
        else:
            self.defaults()
        self.save()
        self.check()

    def save(self):
        config = configparser.ConfigParser()
        config["Paths"] = self.current
        mod_folders = ",".join(self.current["mod_folders"])
        config["Paths"]["mod_folders"] = mod_folders

        with open(self.location, "w+") as configfile:
            config.write(configfile)

    def load(self):
        config = configparser.ConfigParser()
        config.read(self.location)
        ini_paths = {**config["Paths"]}
        print(ini_paths)
        # Add null values for missing keys
        for key in self.default_paths:
            if not key in ini_paths:
                ini_paths[key] = [] if self.key_types[key] == "multiple_dir" else ""
        # Split up "mod_folders" value string
        ini_paths["mod_folders"] = ini_paths["mod_folders"].split(",")
        self.current = ini_paths
        self.remove_invalid()

    def defaults(self):
        self.current = self.default_paths
        self.remove_invalid()

    def remove_invalid(self):
        for key, itype in self.key_types.items():
            if itype == "file":
                if not isfile(self.current[key]):
                    self.current[key] = ""

            elif itype == "dir":
                if not isdir(self.current[key]):
                    self.current[key] = ""

            elif itype == "multiple_dir":
                for i in range(len(self.current[key])-1,-1,-1):
                    if not isdir(self.current[key][i]):
                        print(self.current[key][i])
                        self.current[key].pop(i)
        print(self.current)

    def check(self):
        for key in self.current:
            print("{}: {}".format(key, self.current[key]))

    def get(self, key):
        try:
            return self.current[key]
        except KeyError:
            print("Invalid key: {}".format(key))
            return

    def add_mod_folder(self, folder):
        if isdir(folder):
            if folder not in self.current["mod_folders"]:
                self.current["mod_folders"].append(folder)
                self.save()
            else:
                print("Directory '{}' is already included as a mod folder".format(folder))
        else:
            print("Directory '{}' is not valid".format(folder))

def load_mod_info(mod_folder_paths):
    mod_array = {}

    for mod_folder in mod_folder_paths:
        for mod_num in os.listdir(mod_folder):
            full_path = pjoin(mod_folder, mod_num)

            mod_about_path = pjoin(full_path,"About/About.xml")
            if os.path.isfile(mod_about_path):
                with open(mod_about_path,encoding="utf-8") as f:
                    about_text = f.read()
            else:
                print("Mod {} has no About folder".format(mod_num))
                continue

            mod_info = {}

            # Title, Author, URL, Description
            for key, pattern in (
                ("title", "<name>(.+)</name>"),
                ("author", "<author>(.+)</author>"),
                ("url", "<url>(.+)</url>"),
                ("description", "<description>([\s\S]+)</description>")):

                try:
                    mod_info[key] = re.findall(pattern, about_text)[0]
                except IndexError:
                    mod_info[key] = None

            # Game Version
            if "targetVersion" in about_text:
                try:
                    mod_info["version"] = re.findall(
                        "<targetVersion>\s*([\d.]+)\s*</targetVersion>", about_text)[0]
                except IndexError:
                    print(about_text)
                    return

            elif "supportedVersions" in about_text:
                    mod_info["version"] = str(max([float(x) for x in re.findall(
                        "<li>\s*([0-9.]+)\s*</li>",about_text)]))

            else:
                mod_info["version"] = "?"

            mod_info["full_path"] = full_path

            mod_array[mod_num] = mod_info

    return mod_array

if __name__ == "__main__":
    p = paths()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    test_mod_dir = pjoin(current_dir, "rimworld_mods/content/294100")
    print(test_mod_dir)

    p.add_mod_folder(test_mod_dir)
    info = load_mod_info(p.get("mod_folders"))
    titles = sorted([(num,info[num]["title"],info[num]["version"]) for num in info],key=lambda x:x[1])
    for e in titles:
        print(e)
