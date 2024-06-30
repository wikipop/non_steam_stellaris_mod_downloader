# Upload steam stellaris mods to paradox launcher

first download your mods to a folder using steam cmd.

```bash
./steamcmd.exe
login anonymous
workshop_download_item 281990 123456789
```

Edit `main.py` with the path to the steam and mods folder (line 7-11)

Warning: This script requires your stellaris mod folder to be empty before running but It will not delete any files on their own.

```python
# -> Path to the directory where the steam workshop content is downloaded
steam_download_directory = os.path.abspath(r"C:\Users\wikipop\Downloads\steamapps\workshop\content\281990")

# -> Path to the directory where the paradox mod directory is located
paradox_mod_directory = os.path.abspath(r"C:\Users\wikipop\Documents\Paradox Interactive\Stellaris\mod")
```

Then run the script to upload the mods to the paradox launcher.

```bash
git clone https://github.com/wikipop/stellaris_steamcmd_mods_to_gog
cd stellaris_steamcmd_mods_to_gog
python main.py
```

Disclaimer: This script is provided as is and may not work for all mods. It is recommended to check the mods in the paradox launcher after running the script to ensure they are working correctly.