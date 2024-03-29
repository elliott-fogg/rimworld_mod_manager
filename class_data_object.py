from os.path import join as pjoin
from os.path import isfile, isdir
import os, time, subprocess, re, configparser

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

class data_object():

    default_paths = {
        "root_folder": "C:/Program Files (x86)/Steam/steamapps/common/RimWorld/",
        "executable": "C:/Program Files (x86)/Steam/steamapps/common/RimWorld/RimWorldWin64.exe",
        "mod_folders": ["C:/Program Files (x86)/Steam/steamapps/common/RimWorld/Mods",
            "C:/Program Files (x86)/Steam/steamapps/workshop/content/294100"],
        "mods_config": os.path.expanduser("~/AppData/LocalLow/Ludeon Studios/Rimworld by Ludeon Studios/Config/ModsConfig.xml"),
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
        self.files = {}
        self.files["directories"] = pjoin(CURRENT_DIR, "directories.ini")

        # Temporary Code (Before manual path setting)
        self.set_default_paths()
        if self.paths["mod_folders"] == []:
            self.load_test_files()

        print(self.paths["mod_folders"])

        self.active = []

        # # Eventual code (When manual path setting has been established)
        # if isfile(self.files["directories"]):
        #     self.load_paths()
        # else:
        #     self.set_default_paths()
        # self.save_paths()
        # self.check_paths()

        self.load_mods_config()

        # Mod Info
        self.load_mod_info()


    def load_paths(self):
        config = configparser.ConfigParser()
        config.read(self.files["directories"])
        ini_paths = {**config["Paths"]}
        # Add null values for missing keys
        for key in self.default_paths:
            if not key in ini_paths:
                ini_paths[key] = [] if self.key_types[key] == "multiple_dir" else ""
        # Split up "mod_folders" value string
        ini_paths["mod_folders"] = ini_paths["mod_folders"].split(",")
        self.paths = ini_paths
        self.remove_invalid()

    def set_default_paths(self):
        self.paths = self.default_paths
        self.remove_invalid()

    def save_paths(self):
        config = configparser.ConfigParser()
        config["Paths"] = self.paths
        mod_folders = ",".join(self.paths["mod_folders"])
        config["Paths"]["mod_folders"] = mod_folders

        with open(self.files["directories"], "w+") as configfile:
            config.write(configfile)

    def remove_invalid(self):
        for key, itype in self.key_types.items():
            if itype == "file":
                if not isfile(self.paths[key]):
                    self.paths[key] = ""

            elif itype == "dir":
                if not isdir(self.paths[key]):
                    self.paths[key] = ""

            elif itype == "multiple_dir":
                for i in range(len(self.paths[key])-1,-1,-1):
                    if not isdir(self.paths[key][i]):
                        self.paths[key].pop(i)

    def check_paths(self):
        for key in self.paths:
            print("{}: {}".format(key, self.paths[key]))
        print()

    def get(self, key):
        try:
            return self.paths[key]
        except KeyError:
            print("Invalid key: {}".format(key))
            return

    def add_mod_folder(self, folder):
        if isdir(folder):
            if folder not in self.paths["mod_folders"]:
                self.paths["mod_folders"].append(folder)
                self.save_paths()
            else:
                print("Mod Folder '{}' already included\n".format(folder))
        else:
            print("Directory '{}' is not valid\n".format(folder))

    def load_mod_info(self):
        mod_array = {}
        for mod_folder in self.paths["mod_folders"]:

            for mod_num in os.listdir(mod_folder):

                # Ignore the Core folder (for now, might need for ordering later)
                if mod_num == "Core":
                    continue

                full_path = pjoin(mod_folder, mod_num)
                mod_about_path = pjoin(full_path, "About/About.xml")
                if isfile(mod_about_path):
                    with open(mod_about_path, encoding="utf-8") as f:
                        about_text = f.read()
                else:
                    print("Mod {} in '{}' has no About folder".format(
                        mod_num, mod_folder))
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

                if "/Steam/" in full_path:
                    mod_info["steam"] = True
                    try:
                        with open(full_path + "About/PublishedFileId.txt", "r") as f:
                            fileId = f.read()
                        mod_info["steam_url"] = "steam://url/CommunityFilePage/" + fileId
                    except:
                        mod_info["steam_url"] = ""
                else:
                    mod_info["steam"] = False
                    mod_info["steam_url"] = ""

                mod_info["full_path"] = full_path

                mod_array[mod_num] = mod_info

        self.mods = mod_array
        for key in mod_info:
            print(key, mod_info[key])

    def load_mods_config(self):
        print(self.paths)
        if isfile(self.paths["mods_config"]):
            print("Mod config exists!")
            with open(self.paths["mods_config"],"r") as mcfile:
                contents = mcfile.read()

            active_mods_text = re.findall("<activeMods>([\s\S]*)</activeMods>",contents)[0]

            self.active = []
            for mod in re.findall("<li>(.+)</li>", active_mods_text):
                self.active.append(mod)
            print(self.active)

        else:
            print("Mod Config File '{}' does not exist!!!".format(self.paths["mods_config"]))

    def load_test_files(self):
        self.paths["mod_folders"] = [pjoin(CURRENT_DIR,"test_dirs/mods/294100")]
        self.paths["mods_config"] = pjoin(CURRENT_DIR,"test_dirs/ModsConfig.xml")


# List of ("Name", "iid")



if __name__ == "__main__":
    data = data_object()
    info = data.mods
    titles = sorted([(num,info[num]["title"],info[num]["version"]) for num in info],key=lambda x:x[1])
    for e in titles:
        print(e)
