import os
import json
import shutil
import sys

weaponlist = 'weapon_list.json'
Renamed_EFX = 'Renamed_EFX'
Original_EFX = 'Original_EFX'
EFX_string = ''
written_json = {}
new_efx_list = 'new_efx_list.json'

if not os.path.exists(f"{Renamed_EFX}"): # create folder if it doesn't exist
    print(f'{Renamed_EFX} missing... created folder')
    os.makedirs(f'{Renamed_EFX}')

if not os.path.exists(f"{Original_EFX}"): # create folder if it doesn't exist
    print(f'{Original_EFX} missing... created folder')
    os.makedirs(f'{Original_EFX}') 
    print(f'Exiting program... add EFX to the {Original_EFX} Folder and then run the program again')
    sys.exit() # exits program

with open(weaponlist, 'r') as file: # load nier weapon_list json
    wep_efx_dict = json.load(file)
    print(f'loaded {weaponlist}')

og_efx_list = os.listdir(Original_EFX) # load original efx supplied from directory
print(f'loaded {Original_EFX} files')

for key, value in zip(wep_efx_dict.keys(), og_efx_list):
    EFX_string = key + '.eff' # append .eff to the weapon name string (ex. wp0040 -> wp0040.eff)
    source_path = os.path.join(Original_EFX, value) # original efx path with the original name
    destination_path = os.path.join(Renamed_EFX, EFX_string) # rename efx path with the weapon name
    shutil.copy2(source_path, destination_path) # copy the files
    print(f"EFX: {value}, Weapon: {wep_efx_dict.get(key)}") # print efx name along with the weapon assigned with it
    written_json[value] = wep_efx_dict.get(key) # append the values to a dictionary to save

with open(new_efx_list, 'w') as json_file: # dump new dictionary to json file
    json.dump(written_json, json_file, indent=2)
    print(f'{new_efx_list} written')