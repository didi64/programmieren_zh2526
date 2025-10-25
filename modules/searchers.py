import os
import re
import nbf.searchables
import nbf.helpers
from ipywidgets import Output
from IPython.display import Markdown, display


def _show_results(results, n=5):
    n = min(len(results), n)
    link_widget = Output(layout={'border': '1px solid black'})
    display(link_widget)
    with link_widget:
        display(Markdown('**Results** ({}/{}):  \n'.format(n, len(results))))
    for res in results[:n]:
        s = res['searchable']
        score = int(res['score'])
        with link_widget:
            rel_path = os.path.relpath(s.path_to_file, os.getcwd())
            link = '[({1}) {0}](<{0}>)  '.format(rel_path, score)
            link = Markdown(link)
            display(link)


def _search_words(words, rootdir='/home/studi/work'):
    results = []

    if type(words) is str:
        words = (words,)
    pats = set(re.compile(re.escape(k)) for k in words)

    # iterator
    files = nbf.helpers.file_iter(rootdir,
                                  filetypes=('.ipynb', '.py'),
                                  exclude_dirs=('__pycache__', 'src'),
                                  )
    for fn in files:
        s = nbf.searchables.Searchable(fn)
        d = s.search(pats)

        all_scores = [d[x] for x in pats]
        score = nbf.helpers.get_score(all_scores)

        if not score:
            continue

        res = {'searchable': s,
               'score': score,
               }
        results.append(res)

    results = sorted(results, key=lambda x: x['score'], reverse=True)
    return results


def word_finder(*words, max_res=5, rootdir='/home/studi/work'):
    res = _search_words(words, rootdir=rootdir)
    _show_results(res, n=max_res)


def tag_finder(*args, **kwarg):
    raise NotImplementedError