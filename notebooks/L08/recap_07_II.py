'''
Hilfsfunktionen fuer das Notebook Recap_07_II.ipynb
Behalte diese File im gleichen Ordner wie Recap_07_II.ipynb
'''


def get_rows(ort, plz):
    rows = [tuple(row[:1]+row[2:]) for row in table
            if (ort == row[0] or len(ort) < len(row[0]) and row[0].startswith(ort+' '))
            and plz == row[1]]
    return rows


def get_data(ortsname):
    return {(ortsname, plz): get_rows(ortsname, plz) for plz in ort_plzs[ortsname]}


def show_data(data):
    width = max(len(str(k)) for k in data) + 1
    for k, v in data.items():
        if len(v) == 1:
            print(f'{str(k).ljust(width)} {v[0]}')
        else:
            print(f'{str(k).ljust(width)} {v[0]}')
            for w in v[1:]:
                print(f'{''.ljust(width)} {w}')


def show(ort):
    show_data(get_data(ort))


def distance(v, w):
    return round(((w[0]-v[0])**2 + (w[1]-v[1])**2)**.5)


def distances(ortsname):
    plzs = ort_plzs[ortsname]
    coords = [get_rows(ortsname, plz)[0][-1] for plz in plzs]
    return [distance(v, w) for v, w in zip(coords, coords[1:])]
