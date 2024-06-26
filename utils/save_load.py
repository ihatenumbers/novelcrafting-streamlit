import json
from os.path import join

def save_json(path, data, mode='w'):
    with open(path, mode) as f:
        json.dump(data, f, indent=2)
        if mode == 'a':
            f.write('\n')

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def list_files_in_dir(path):
    from os import listdir
    from os.path import isfile, join
    return [f for f in listdir(path) if isfile(join(path, f))]

def list_chapters_in_file(path):
    data = load_json(path)['chapters']
    for i in range(len(data)):
        data[i] = {'title': data[i]['title'], 'content': data[i]['content']}
    return data
