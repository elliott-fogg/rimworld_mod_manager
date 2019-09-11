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

    key_types = (
        ("root_folder","dir"),
        ("executable","file"),
        ("mods_config","file"),
        ("version", "file"),
        ("mod_folders","multiple_dir")
    )

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
        config["Paths"]["mod_folders"] = ",".join(config["Paths"]["mod_folders"])

        with open(self.location, "w+") as configfile:
            config.write(configfile)

    def load(self):
        config = configparser.ConfigParser()
        config.read(self.location)
        ini_paths = {**config["Paths"]}
        # Add null values for missing keys
        for key in self.default_paths:
            if not key in ini_paths:
                ini_paths[key] = [] if key_types[key] == "multiple_dir" else ""
        # Split up "mod_folders" value string
        ini_paths["mod_folders"] = ini_paths["mod_folders"].split(",")
        self.current = ini_paths
        self.remove_invalid()

    def defaults(self):
        self.current = self.default_paths
        self.remove_invalid()

    def remove_invalid(self):
        for key, itype in self.key_types:
            if itype == "file":
                if not isfile(self.current[key]):
                    self.current[key] = ""

            elif itype == "dir":
                if not isdir(self.current[key]):
                    self.current[key] = ""

            elif itype == "multiple_dir":
                for i in range(len(self.current[key])-1,-1,-1):
                    if not isdir(self.current[key][i]):
                        self.current[key].pop(i)

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
            self.current["mod_folders"].append(folder)
            self.save()
        else:
            print("Directory '{}' is not valid".format(folder))

# def set_directories():
#     current_paths = {}
#     current_dir = os.path.abspath(os.path.dirname(__file__))
#     directories_file = pjoin(current_dir, "directories.ini")
#
#     current_paths = default_paths.copy()
#
#     # Load the .ini file (if it exists)
#     if isfile(directories_file):
#         config = configparser.ConfigParser()
#         config.read(directories_file)
#         ini_paths = {**config["Paths"]}
#         try:
#             if ini_paths["mod_folders"] != "":
#                 ini_paths["mod_folders"] = \
#                     ini_paths["mod_folders"].split(",")
#             else:
#                 ini_paths["mod_folders"] = []
#
#         except KeyError:
#             pass
#
#         current_paths.update(ini_paths)
#
#     # Check that all paths are valid - remove invalid paths
#     for key, itype in key_types:
#         if itype == "file":
#             if not isfile(current_paths[key]):
#                 current_paths[key] = ""
#
#         elif itype == "dir":
#             if not isdir(current_paths[key]):
#                 current_paths[key] = ""
#
#         elif itype == "multiple_dir":
#             print(current_paths[key])
#             for i in range(len(current_paths[key])-1,-1,-1):
#                 if not isdir(current_paths[key][i]):
#                     current_paths[key].pop(i)
#
#     # Print paths to check - REMOVE
#     for key in current_paths:
#         print("{}: {}".format(key,current_paths[key]))
#
#     # Save .ini file
#     save_paths(current_paths, directories_file)
#     config["Paths"] = current_paths
#     config_output = current_paths
#
#     return current_paths

    #
    # # Check for existing .ini file
    # if isfile(directories_file):
    #     config.read(directories_file)
    #     for key, itype in key_types:
    #         try:
    #             current_paths["key"] = test_paths(config["Paths"][key], itype)
    #         except KeyError:
    #             current_paths[key] = ""
    #     if current_paths["mod_folders"] == "":
    #         current_paths["mod_folders"] = []
    #
    # # Check for existing .ini file
    # ## Check if ini file exists
    # ## If it does, check that all keys exist
    # ## If they do, check that each key is valid
    #
    # # if isfile(directories_file):
    # #     config.read(directories_file)
    # #     for key in ("root_folder","executable","mods_config"):
    # #         if key in config["Paths"]:
    # #             current_paths[key] = config["Paths"][key]
    # #         else:
    # #             current_paths[key] = ""
    # #     if mod_folders in config["Paths"]:
    #
    # if False:
    #     pass
    #
    # else:
    #     # No existing .ini file. Check defaults
    #     if isdir(default_paths["root_folder"]):
    #         current_paths["root_folder"] = default_paths["root_folder"]
    #     else:
    #         current_paths["root_folder"] = ""
    #
    #     if isfile(default_paths["executable"]):
    #         current_paths["executable"] = default_paths["executable"]
    #     else:
    #         current_paths["executable"] = ""
    #
    #     if isfile(default_paths["mods_config"]):
    #         current_paths["mods_config"] = default_paths["mods_config"]
    #     else:
    #         current_paths["mods_config"] = ""
    #
    #     if isfile(default_paths["version"]):
    #         current_paths["version"] = default_paths["version"]
    #     else:
    #         current_paths["version"] = ""
    #
    #     current_paths["mod_folders"] = []
    #     for mod_folder in default_paths["mod_folders"]:
    #         if isdir(mod_folder):
    #             current_paths["mod_folders"].append(mod_folder)
    #
    # config["Paths"] = current_paths
    # with open(directories_file,"w+") as configfile:
    #     config.write(configfile)
    #
    # return current_paths

# def add_mod_folder(path):

def load_mod_info(mod_folder_paths):
    pass


def load_mod_info(mod_folder_paths):
    mod_array = {}

    for mod_folder in mod_folder_paths:
        print(mod_folder)
        for mod_num in os.listdir(mod_folder):
            full_path = pjoin(mod_folder, mod_num)
            print(full_path)

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
    # titles = sorted([(num,info[num]["title"],info[num]["version"]) for num in info],key=lambda x:x[1])
    # for e in titles:
    #     print(e)
