import json
import os
from filetools import file_iter


def add_tags(path_to_notebook, tags, append=False, overwrite=False):
    '''path_to_notebook: path to a .ipynb file (notebook)
       tags: tuple[str]
       adds {tags: [tag1, ..., tag_n]} a metadata to the notebook, 
            appends to existing tag list if append=True
    '''
    assert all(type(tag) is str for tag in tags), 'tags must be strings'
    with open(path_to_notebook, 'r') as f:
        data = json.load(f)
        data['metadata'].setdefault('author', 'Dieter Probst')
        tagset = set(data['metadata'].setdefault('tags', [])) if append else set()
        tags = sorted(tagset | set(tags))
        data['metadata']['tags'] = tags
        # print(data['metadata']['tags'])
    with open(path_to_notebook, 'w') as f:
        json.dump(data, f)
    return data


def get_tags(path_to_notebook):
    '''path_to_notebook: path to .ipynb file (notebook)
       return: set[str] the tags of the notebook
    '''
    with open(path_to_notebook, 'r') as f:
        data = json.load(f)
        tags = set(data['metadata'].setdefault('tags', []))
    return tags


def get_taginfo(root, comment_out=False):
    '''root: project_root
             must have a file tags.txt with the tag information
    '''
    tag_info = {}

    tag_file = f'{root}/tags.txt'
    with open(tag_file, 'r') as f:
        lines = f.readlines()

    section = ''
    for line in lines:
        line = line.strip()
        if not line or line[0] == '#':
            continue
        if line[0] == '@':
            section = line[1:].split()[0]
            continue
        file, tags = line.split(':')
        file = file.strip()
        tags = tuple(tag for tag in tags.split(',') if tag)
        tag_info[file] = (section, tags)

    if comment_out:
        lines = ['# ' + line if not line.lstrip().startswith('#') else line for line in lines]
        with open(tag_file, 'w') as f:
            f.writelines(lines)

    return tag_info


def tagger(project_root):
    '''root: project_root
             must have a file tags.txt with the tag information
      adds the tags from tags.txt to the notebooks
    '''
    tag_dict = get_taginfo(project_root, comment_out=True)
    for nb_path in file_iter(project_root):
        nb = os.path.basename(nb_path)
        if nb not in tag_dict:
            continue
        section, tags = tag_dict[nb]
        # print(f'file: {nb}, section: {section}, tags: {tags}')
        add_tags(nb_path, (section,) + tags)


def tag_finder(project_root, tags):
    '''root: project_root
             must have a file tags.txt with the tag information
       tags: tuple[str]
    '''
    assert all(type(tag) is str for tag in tags), 'tags must be strings'
    tags = set(tags)
    results = []
    for nb_path in file_iter(project_root):
        if tags.issubset(get_tags(nb_path)):
            results.append(nb_path)
    return sorted(results)