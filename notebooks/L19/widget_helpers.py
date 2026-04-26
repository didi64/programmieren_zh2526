'''
Modul mit Methoden zum raschen Erstellen der gebraechlichsten Jupyterlab-Widgets'
Benutze folgende Line-Magic fuer eine Demo:
%run -m widget_helpers
'''
from ipycanvas import Canvas, MultiCanvas
from ipywidgets import Output


LAYOUT = {'border': '1px solid black'}


def get_out():
    '''Gibt ein Output-Widget mit layout=LAYOUT zurueck'''
    out = Output(layout=LAYOUT)
    return out


def get_canvas(width=100, height=100):
    '''gibt ein Canvas-Widget mit layout=LAYOUT zurueck'''
    canvas = Canvas(width=width, height=height, layout=LAYOUT)
    return canvas


def get_mcanvas(n=2, width=100, height=100):
    '''gibt ein MultiCanvas-Widget mit layout=LAYOUT zurueck'''
    mcanvas = MultiCanvas(n, width=width, height=height, layout=LAYOUT)
    return mcanvas


if __name__ == '__main__':
    from IPython.display import display


    out = get_out()
    with out:
        print('- get_out() returns an Output-Widget')
        print('- get_canvas(width=100, height=100) returns a Canvas-Widget')
        print('- get_mcanvas(n=2, width=100, height=100) returns a MultiCanvas-Widget with 2 layers')

    canvas = get_canvas(100, 50)
    canvas.font = '50px sans serif'
    canvas.text_align = 'center'
    canvas.fill_style = 'blue'
    canvas.fill_text('Canvas', 50, 50, max_width=100)

    mcanvas = get_mcanvas(2, 100, 50)
    bg, fg = mcanvas
    bg.fill_rect(0, 0, mcanvas.width, mcanvas.height)
    fg.fill_style = 'red'
    fg.fill_circle(mcanvas.width/2, mcanvas.height/2, min(mcanvas.width/3, mcanvas.height/3))

    display(canvas, mcanvas, out)