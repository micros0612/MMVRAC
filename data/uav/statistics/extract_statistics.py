import os
from tqdm import tqdm

def extract_info_and_save(file_name):
    # Count total lines in the file to set up the progress bar
    total_lines = sum(1 for _ in open(file_name, 'r', encoding='utf-8'))

    # Open the input file
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Open all output files
    with    open('PersonID.txt', 'w', encoding='utf-8') as person_id_file, \
            open('setup.txt', 'w', encoding='utf-8') as setup_file, \
            open('Gender.txt', 'w', encoding='utf-8') as gender_file, \
            open('Backpack.txt', 'w', encoding='utf-8') as backpack_file, \
            open('Hat.txt', 'w', encoding='utf-8') as hat_file, \
            open('UpperClothing.txt', 'w', encoding='utf-8') as upper_clothing_file, \
            open('LowerClothing.txt', 'w', encoding='utf-8') as lower_clothing_file, \
            open('label.txt', 'w', encoding='utf-8') as label_file, \
            open('Replicate.txt', 'w', encoding='utf-8') as replicate_file, \
            open('timestamp.txt', 'w', encoding='utf-8') as timestamp_file:

        # Iterate over lines with tqdm for progress bar
        for line in tqdm(lines, total=total_lines, desc='Processing'):
            # Extract information from each line
            person_id = line[line.find('P') + 1:line.find('P') + 4]
            setup = line[line.find('S') + 1:line.find('S') + 4]
            gender = line[line.find('G') + 1:line.find('G') + 3]
            backpack = line[line.find('B') + 1:line.find('B') + 3]
            hat = line[line.find('H') + 1:line.find('H') + 3]
            upper_clothing = line[line.find('UC') + 2:line.find('UC') + 8]
            lower_clothing = line[line.find('LC') + 2:line.find('LC') + 8]
            label = line[line.find('A') + 1:line.find('A') + 4]
            replicate = line[line.find('R') + 1:line.find('R') + 4]
            timestamp = line[line.find('_') + 1:line.find('.')]

            # Write information to respective files
            person_id_file.write(f'{person_id}\n')
            setup_file.write(f'{setup}\n')
            gender_file.write(f'{gender}\n')
            backpack_file.write(f'{backpack}\n')
            hat_file.write(f'{hat}\n')
            upper_clothing_file.write(f'{upper_clothing}\n')
            lower_clothing_file.write(f'{lower_clothing}\n')
            label_file.write(f'{label}\n')
            replicate_file.write(f'{replicate}\n')
            timestamp_file.write(f'{timestamp}\n')


file_path = '/opt/data/private/MMVRAC/LST/data/uav/statistics/skes_available_name.txt'
ignored_file_path = '/opt/data/private/MMVRAC/LST/data/uav/statistics/ignored_list.txt'

# Read ignored joints
ignored_joints = []
if os.path.exists(ignored_file_path):
    with open(ignored_file_path, "r", encoding="utf-8") as ignored_file:
        ignored_joints = ignored_file.read().splitlines()

if not os.path.exists(file_path):
    # Specify the folder path
    folder_path = '/opt/data/private/MMVRAC/datasets/ori_skeleton'
    # Get all file names in the folder
    file_names = os.listdir(folder_path)
    # Write file names to a file
    with open(file_path, "w", encoding="utf-8") as file:
        for name in file_names:
            # Remove dot and characters after it
            modified_name = name.split('.')[0]
            if modified_name not in ignored_joints:
                file.write(modified_name + "\n")

# Extract information and save from skes_available_name.txt
extract_info_and_save(file_path)
