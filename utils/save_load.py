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
    data = load_json(path)
    data = data['chapters']
    for i in range(len(data)):
        data[i] = {'title': data[i]['title'], 'content': data[i]['content']}
    return data

def add_chapter(path, title):
    data = load_json(path)
    data['chapters'].append({'title': title, 'content': ''})
    save_json(path, data)

def delete_chapter(path, title):
    data = load_json(path)
    for i in range(len(data)):
        if data['chapters'][i]['title'] == title:
            save_json(join('stories', 'deleted', 'deleted-chapters.json'), data['chapters'][i], mode='a')
            data['chapters'].pop(i)
            break
    save_json(path, data)