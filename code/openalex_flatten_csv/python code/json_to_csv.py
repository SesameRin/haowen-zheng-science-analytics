import json
import os
import gzip
import shutil


def txt_to_list(txt_path, reformat):
    formatted_dict_list = []
    with open(txt_path, 'r', encoding='utf-8') as f:
        cnt = 0
        for line in f:
            old_dict = json.loads(line)
            formatted_dict = reformat(old_dict)
            formatted_dict_list.append(formatted_dict)
            cnt += 1
            if (cnt == 500):
                break
    return formatted_dict_list

def process_files(directory,txt_to_list,reformat):
    all_data = []
    break_flag = False
    for root, dirs, files in os.walk(directory):
        if (break_flag):
            break
        for file in files:
            if (break_flag):
                break
            if file.endswith('.gz'):
                # Get full file path.
                file_path = os.path.join(root, file)

                # Create .txt file path.
                txt_path = os.path.splitext(file_path)[0] + '.txt'

                # Decompress .gz file.
                with gzip.open(file_path, 'rb') as f_in:
                    with open(txt_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                # Add data to the main list.
                all_data.extend(txt_to_list(txt_path,reformat))

                # Optional: remove .txt file after reading it.
                os.remove(txt_path)
            print('record length: ', len(all_data))
            if (len(all_data) > 5000): # treshold to limit the number of records
                break_flag = True

    return all_data
