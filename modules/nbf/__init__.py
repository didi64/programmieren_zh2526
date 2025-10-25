import os
from .nb_searcher import NBSearcher
from .view import View
from .controller import Controller
from IPython.core.display_functions import display


def run(root=None):
    if root is None:
        root = '/home/studi/work'
    if root.isnumeric():
        n = int(root)
        root = os.path.join(os.curdir, *[os.pardir]*n)

    nbs = NBSearcher(root=root)
    display(Controller(nbs), View(nbs))