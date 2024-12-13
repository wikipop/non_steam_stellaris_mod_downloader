# Upload steam stellaris mods to paradox launcher

This script will help you with downloading mods to your non steam version of Stellaris.
Script is configured to work  out of the box with stellaris, but you can easily modify it to work with other games (like hoi4).

## Installation
1. Download the script
```bash
git clone https://github.com/wikipop/stellaris_steamcmd_mods_to_gog.git
```

2. Install [Py-SteamCMD-Wrapper](https://github.com/wmellema/Py-SteamCMD-Wrapper) module
```bash
pip install py-steamcmd-wrapper
```

## Usage
1. Edit `mods_to_download.txt` file and add steam workshop ids of the mods you want to download.

2. Run the script
```bash
python stellaris_steamcmd_mods_to_gog.py
```

3. First run 3rd option to download selected mods
```bash
What would you like to do?
3. Download mods
```

4. After downloading the mods, run 1st option to move them to the paradox mod directory
```bash
What would you like to do?
1. Update (clean and copy) mods from steam workshop to paradox mod directory
```

This option will require you to clean the paradox mod directory, **but script will not delete anything on their own**. 

If you want to keep the mods that are already in the paradox mod directory, you can use the 2nd option instead.

```bash
What would you like to do?
2. Update (only add new) existing mods in paradox mod directory
```

## Troubleshooting
If your stellaris mod directory is not located in the default location, you can change the path in the script.

Lines 6-13 in `stellaris_steamcmd_mods_to_gog.py`:
```python
# -> Path to the directory where the paradox mod directory is located
PARADOX_MOD_DIRECTORY = os.path.abspath(str(pathlib.Path.home()) + r"\Documents\Paradox Interactive\Stellaris\mod")

# -> Path to the directory where the steam workshop content will be downloaded
STEAM_TEMP_DIRECTORY = os.path.abspath(str(pathlib.Path.home()) + r"\Downloads\stellaris_mod_temp")

# -> Path to the directory where exactly the steam workshop content is stored
STEAM_DOWNLOAD_DIRECTORY = STEAM_TEMP_DIRECTORY + r"\steamapps\workshop\content\281990"
```

If you have any issues with the script, feel free to open an issue on the github page.