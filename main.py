import os
import pathlib
import zipfile
from shutil import copytree as copy_tree

# -> Path to the directory where the paradox mod directory is located
PARADOX_MOD_DIRECTORY = os.path.abspath(str(pathlib.Path.home()) + r"\Documents\Paradox Interactive\Stellaris\mod")

# -> Path to the directory where the steam workshop content will be downloaded
STEAM_TEMP_DIRECTORY = os.path.abspath(str(pathlib.Path.home()) + r"\Downloads\stellaris_mod_temp")

# -> Path to the directory where exactly the steam workshop content is stored
STEAM_DOWNLOAD_DIRECTORY = STEAM_TEMP_DIRECTORY + r"\steamapps\workshop\content\281990"

header_message = """# Provide in this file the list of mod ids you want to download.
# In order to get the id of a workshop mod, go to its workshop site, and look at the numbers after ?id of its URL, That's your mod's id.
# So for https://steamcommunity.com/sharedfiles/filedetails/?id=1682700568, the ID would be 1682700568.
# Your link can also look like https://steamcommunity.com/sharedfiles/filedetails/?id=2250100617&searchtext=Ultimate+Automation
# In this case, the ID would be 2250100617.
#
# In next 3 lines you can see examples of how to write the mod ids in the file.
# Delete them before adding your own mod ids.\n"""

def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def list_all(directory):
    return [f for f in os.listdir(directory)]


def verify_directories():
    flag_steam = True
    flag_paradox = True
    if not os.path.exists(STEAM_TEMP_DIRECTORY):
        print("[Wrong Configuration] - Steam download directory does not exist.")
        print("Provided directory:", STEAM_TEMP_DIRECTORY)
        print("Do you want to create the directory? (y/n)")
        user_choice = input()
        if user_choice.lower() == "y":
            os.makedirs(STEAM_TEMP_DIRECTORY)
            print("Directory created successfully")
        else:
            flag_steam = False

    if not os.path.exists(PARADOX_MOD_DIRECTORY):
        print("[Wrong Configuration] - Paradox mod directory does not exist.")
        print("Provided directory:", PARADOX_MOD_DIRECTORY)
        print("Do you want to create the directory? (y/n)")
        user_choice = input()
        if user_choice.lower() == "y":
            os.makedirs(PARADOX_MOD_DIRECTORY)
            print("Directory created successfully")
        else:
            flag_paradox = False

    return flag_steam and flag_paradox

def modify_descriptor_file(descriptor_file_raw_data: str, mod_id: str):
    # split the data by new line
    data = descriptor_file_raw_data.split("\n")

    for line in data:
        if line.startswith("path"):
            data.remove(line)
            break

    data.insert(-1, f"path=\"{PARADOX_MOD_DIRECTORY}/{mod_id}\"")
    new_file = "\n".join(data)
    new_file = new_file.replace(os.sep, "/")

    return new_file


def update_mods():
    source_mod_folders = list_all(STEAM_DOWNLOAD_DIRECTORY)

    for mod_id in source_mod_folders:

        if (mod_id + ".mod") in list_files(PARADOX_MOD_DIRECTORY):
            print(f"Mod {mod_id} already exists in paradox mod directory")
            continue

        print("Copying " + mod_id)
        steam_mod_folder = pathlib.Path(STEAM_DOWNLOAD_DIRECTORY + "\\" + mod_id)

        # check if in source is zipped file

        for file in list_all(steam_mod_folder):
            if file.endswith(".zip"):
                print("Found zipped file")
                # unzip file
                with zipfile.ZipFile(steam_mod_folder / file, 'r') as zip_ref:
                    zip_ref.extractall(steam_mod_folder)

        descriptor_file = steam_mod_folder / "descriptor.mod"

        # copy descriptor file to new directory as "mod_id".mod

        output_dot_mod_file = pathlib.Path(PARADOX_MOD_DIRECTORY + "\\" + mod_id + ".mod")
        with open(descriptor_file, 'r') as file:
            data = file.read()
            data = modify_descriptor_file(data, mod_id)
            with open(output_dot_mod_file, 'w') as new_file:
                new_file.write(data)

        # copy steam_mod_folder to new directory

        output_mod_folder = pathlib.Path(PARADOX_MOD_DIRECTORY + "\\" + mod_id)
        copy_tree(str(steam_mod_folder), str(output_mod_folder))

    print("All mods updated successfully")

def update_n_clean():
    if len(list_all(PARADOX_MOD_DIRECTORY)) != 0:
        print("Mod directory is not empty")
        print("Before copying the files, please make sure that the mod directory is empty")
        os.system("explorer " + PARADOX_MOD_DIRECTORY)
        exit()

    update_mods()


def create_download_list():
    mod_ids = []

    with open("mods_to_download.txt", "r") as file:
        for line in file:
            if not line.startswith("#"):
                mod_ids.append(line.strip())

    choice = input("Do you want to add existing mods to the list? (y/n): ")
    if choice.lower() == "y":
        for mod in list_files(PARADOX_MOD_DIRECTORY):
            mod_id = mod.split(".")[0]
            if mod_id not in mod_ids:
                mod_ids.append(mod_id)

    with open("mods_to_download.txt", "w") as file:
        # Delete the content of the file
        file.seek(0)
        file.truncate(0)

        file.write(header_message)

        for mod_id in mod_ids:
            file.write(mod_id + "\n")

    return mod_ids


def download_mods():
    from pysteamcmdwrapper import SteamCMD
    from pysteamcmdwrapper import SteamCMDException
    os.makedirs("steamcmd", exist_ok=True)
    steam = SteamCMD("steamcmd")
    try:
        print("Installing steam cmd...")
        steam.install()
        print("Steam cmd installed")
    except SteamCMDException:
        print("Steam cmd already installed")

    mods_to_download = create_download_list()

    if "111111111" in mods_to_download:
        print("Please remove the example mod id from the file")
        exit()

    for mod_id in mods_to_download:
        print("Downloading mod " + mod_id)
        steam.workshop_update(281990, mod_id, install_dir=STEAM_TEMP_DIRECTORY, validate=True)

    print("All mods downloaded successfully")

def main():
    if not verify_directories():
        exit()
    print("")
    print("What would you like to do?")
    print("1. Update (clean and copy) mods from steam workshop to paradox mod directory")
    print("2. Update (only add new) existing mods in paradox mod directory")
    print("3. Download mods")
    print("4. Exit")
    choice = input("Enter your choice: ")

    match choice:
        case "1":
            update_n_clean()
        case "2":
            pass
            update_mods()
        case "3":
            pass
            download_mods()
        case "4":
            exit()
        case _:
            print("Invalid choice")

    main()

if __name__ == '__main__':
    main()