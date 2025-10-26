import os


def find_file(rootdir, name, exclude_dirs=('__pycache__',), hidden_dir=False):
    '''return: list of all paths to a file with the given name
       all files with the given filetyes below the rootdir,
       skips all exclude_dirs and hidden directories if hidden_dir=False
    '''
    results = []
    for root, folders, files in os.walk(rootdir):
        results += [os.path.join(root, f) for f in files if f == name]
        folders[:] = [f for f in folders if (hidden_dir or not f.startswith('.')) and f not in exclude_dirs]
    return results


def file_iter(rootdir, filetypes=('.ipynb',), exclude_dirs=('__pycache__',), hidden_dir=False):
    '''return: iterator
       all files with the given filetyes below the rootdir,
       skips all exclude_dirs and hidden directories if hidden_dir=False
    '''
    for root, folders, files in os.walk(rootdir):
        matches = [os.path.join(root, f) for f in files if os.path.splitext(f)[1] in filetypes]
        folders[:] = [f for f in folders if (hidden_dir or not f.startswith('.')) and f not in exclude_dirs]
        yield from matches