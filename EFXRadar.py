import os
import json
import shutil
import sys
import subprocess

def folder_check(folder): #checks for a folder and creates it if it doesn't exist
    if not os.path.exists(folder):
        try: 
            os.mkdir(folder) 
            print(f'{folder} missing... created folder')
        except OSError as error: 
            print(error)  

def main():
    weaponlist = 'weapon_list.json'
    new_efx_list = 'new_efx_list.json'
    Renamed_EFX_Output = 'Renamed_EFX_Output'
    Original_EST = 'Original_EST'
    est_string = '001.est'
    Packer_Folder = 'Packer_Folder' + '\\'
    written_json = {} 
    Header_BXM = 'header.bxm'
    DAT_Packer = 'DATrepacker-master\\' + 'dat.py'

    folder_check(Renamed_EFX_Output) # create folder if it doesn't exist

    if not os.path.exists(Original_EST):  # create folder if it doesn't exist
        folder_check(Original_EST)
        print(f'Exiting program... add EFX to the {Original_EST} Folder and then run the program again')
        sys.exit()  # exits program

    with open(weaponlist, 'r') as file:  # load nier weapon_list json
        wep_efx_dict = json.load(file)
        print(f'loaded {weaponlist}')

    print(f'copying ' + Header_BXM + ' to all wpfolders')
    for key in wep_efx_dict: # creates weapon folders for repacking then move the header.bxm into all of them
        wpfolder = Packer_Folder + key # combines packer folder string + weapon_json name to make Packer_Folder\Weapon folder string

        folder_check(wpfolder) # if that path doesn't exist it's created

        source_path = os.path.join(Packer_Folder, Header_BXM)  # original source of bxm
        destination_path = os.path.join(wpfolder, Header_BXM)  # weapon folders
        shutil.copy2(source_path, destination_path)  # copy the files

    og_est_list = os.listdir(Original_EST)  # load original efx supplied from directory
    print(f'loaded {Original_EST} files')

    print('copying and renaming ests...')
    for key, est in zip(wep_efx_dict.keys(), og_est_list): # take original est, rename it to 001.est, place it in wp folder ex. 629.est -> 001.est
        wpfolder = Packer_Folder + key

        source_path = os.path.join(Original_EST, est)  # original est path with the original name
        destination_path = os.path.join(wpfolder, est_string)  # wp weapon folder with new name
        shutil.copy2(source_path, destination_path)  # copy the files and rename

        print(f"{est} -> Weapon: {wep_efx_dict.get(key)}")  # print efx name along with the weapon assigned with it
        written_json[est] = wep_efx_dict.get(key)  # append the ests to a dictionary to save

    print('packing files...')
    for key, est in zip(wep_efx_dict.keys(), og_est_list): # pack folders and then move them
        wpfolder = Packer_Folder + key
        wpfolder_dat = key + '.dat'
        wpfolder_eff = key + '.eff'
        command = ['python', DAT_Packer, wpfolder] # create command ex. python dat.py Packer_folder\wp0030

        try:
            subprocess.run(command, check=True)  # run command and pack folder, raise exception if non-zero exit code
        except subprocess.CalledProcessError as e:
            print(f"Error in subprocess: {e}")
            break  # Break out of the loop if an error occurs
        source_path = os.path.join(Packer_Folder, wpfolder_dat)  # packed eff.dat
        destination_path = os.path.join(Renamed_EFX_Output, wpfolder_eff)  # move to renamed_efx folder with new name
        shutil.move(source_path, destination_path)  # copy the files and rename

    with open(new_efx_list, 'w') as json_file:  # dump new dictionary to json file
        json.dump(written_json, json_file, indent=2)
        print(f'{new_efx_list} written')

if __name__ == "__main__":
    main()
