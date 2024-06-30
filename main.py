import os
import pathlib
import zipfile
from distutils.dir_util import copy_tree

# -> Path to the directory where the steam workshop content is downloaded
steam_download_directory = os.path.abspath(r"C:\Users\wikipop\Downloads\steamapps\workshop\content\281990")

# -> Path to the directory where the paradox mod directory is located
paradox_mod_directory = os.path.abspath(r"C:\Users\wikipop\Documents\Paradox Interactive\Stellaris\mod")


# For example:
# steam_download_directory = "C:\Users\user\Downloads\steamapps\workshop\content\281990"
# paradox_mod_directory = "C:\Users\user\Documents\Paradox Interactive\Stellaris\mod"


def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def list_all(directory):
    return [f for f in os.listdir(directory)]


def modify_descriptor_file(descriptor_file_raw_data: str, mod_id: str):
    # split the data by new line
    data = descriptor_file_raw_data.split("\n")

    data.insert(-2, f"path={paradox_mod_directory}\\{mod_id}")

    new_file = "\n".join(data)

    return new_file


def copy_mods():
    if len(list_all(paradox_mod_directory)) != 0:
        print("Mod directory is not empty")
        print("Before copying the files, please make sure that the mod directory is empty")
        os.system("explorer " + paradox_mod_directory)
        exit()

    source_mod_folders = list_all(steam_download_directory)

    for mod_id in source_mod_folders:
        print("Copying " + mod_id)
        steam_mod_folder = pathlib.Path(steam_download_directory + "\\" + mod_id)

        # check if in source is zipped file

        for file in list_all(steam_mod_folder):
            if file.endswith(".zip"):
                print("Found zipped file")
                # unzip file
                with zipfile.ZipFile(steam_mod_folder / file, 'r') as zip_ref:
                    zip_ref.extractall(steam_mod_folder)

        descriptor_file = steam_mod_folder / "descriptor.mod"

        # copy descriptor file to new directory as "mod_id".mod

        output_dot_mod_file = pathlib.Path(paradox_mod_directory + "\\" + mod_id + ".mod")
        with open(descriptor_file, 'r') as file:
            data = file.read()
            data = modify_descriptor_file(data, mod_id)
            with open(output_dot_mod_file, 'w') as new_file:
                new_file.write(data)

        # copy steam_mod_folder to new directory

        output_mod_folder = pathlib.Path(paradox_mod_directory + "\\" + mod_id)
        copy_tree(str(steam_mod_folder), str(output_mod_folder))


if __name__ == '__main__':
    print("What would you like to do?")
    print("1. Copy mods from steam workshop to paradox mod directory")
    print("2. Update existing mods in paradox mod directory")
    print("3. Exit")
    choice = input("Enter your choice: ")

    match choice:
        case "1":
            copy_mods()
        case "2":
            pass
            # update_mods()
        case "3":
            exit()
        case _:
            print("Invalid choice")
            exit()
