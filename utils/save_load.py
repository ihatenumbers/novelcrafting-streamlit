import json

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
        # f.write('\n')

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def list_files_in_dir(path):
    from os import listdir
    from os.path import isfile, join
    return [f for f in listdir(path) if isfile(join(path, f))]

def list_chapters_in_file(path):
    data = load_json(path)
    data = data['chapters']
    for i in range(len(data)):
        data[i] = {'title': data[i]['title'], 'content': data[i]['content']}
    return data