import math
from math import pi as PI
from vector import Vector as Vec
from datetime import datetime


def get_arrow_tip(start, end, tip_size=5, tip=((-2, 1), (-2, -1), (0, 0))):
    '''gibt die Punkte der Pfeilspitze als Tuple zurueck
       die Pfeilspitze liegt bei end des Pfeils von start nach end
       size ist Laenge der Pfeilspitze
    '''
    arrow = Vec(*end) - Vec(*start)
    alpha = math.atan2(arrow.y, arrow.x)

    pts = Vec.transform(tip, end, alpha, tip_size)
    return pts


def draw_arrow(canvas, start, end, tip_size=5, line_width=1,
               color='black', tip_color='red'):
    '''zeichnet einen Pfeil von start nach end auf canvas'''
    pts = get_arrow_tip(start, end, tip_size)

    canvas.save()
    canvas.line_width = line_width
    canvas.stroke_style = color
    canvas.fill_style = tip_color
    canvas.stroke_line(*start, *end)
    canvas.fill_polygon(pts)
    canvas.restore()


def draw_clockface(canvas, center, radius):
    '''zeichet ein Zifferblatt am Punkt center mit geg. radius'''
    marks = [(math.cos(i*PI/30), math.sin(i*PI/30)) for i in range(60)]
    starts = Vec.transform(marks, center, scale=0.9*radius)
    ends = Vec.transform(marks, center, scale=1.1*radius)

    lines = [[start, end] for start, end in zip(starts, ends)]

    canvas.save()
    for i, line in enumerate(lines):
        if i % 5 == 0:
            canvas.line_width = 3
            canvas.stroke_style = 'blue'
        else:
            canvas.line_width = 1
            canvas.stroke_style = 'black'

        canvas.stroke_lines(line)

    canvas.restore()


def draw_hour_hand(canvas, center, radius, hour, minute):
    '''zeichnet den Stundenzeiger , passend auf
       ein Zifferblatt an Pos. center mit geg. radius
    '''
    alpha = 2*PI*(hour % 12) / 12 + 2*PI*minute/60/12
    hand = 0.4*radius*(-Vec.e2).rotate(alpha) + Vec(*center)

    canvas.save()
    canvas.fill_style = 'black'
    canvas.line_width = 3
    canvas.stroke_line(*center, *hand.as_tuple())

    canvas.restore()


def draw_minute_hand(canvas, center, radius, minute):
    '''zeichnet den Minutenzeiger'''
    alpha = 2*PI*minute / 60
    hand = 0.6*radius*(-Vec.e2).rotate(alpha) + Vec(*center)

    canvas.save()
    canvas.fill_style = 'black'
    canvas.line_width = 2
    canvas.stroke_line(*center, *hand.as_tuple())

    canvas.restore()


def draw_second_hand(canvas, center, radius, second):
    '''zeichnet den Sekundenzeiger'''
    alpha = 2*PI*second / 60
    tip = 0.8*radius*(-Vec.e2).rotate(alpha) + Vec(*center)
    draw_arrow(canvas, center, tip.as_tuple())


def get_time():
    now = datetime.now()
    hours = now.hour
    minutes = now.minute
    seconds = now.second
    return hours, minutes, seconds


def draw_hands(canvas, center, radius, hms=None):
    '''erfragt die Uhrzeit und zeichnet die Uhrzeiger, passend auf
       ein Zifferblatt an Pos. center mit geg. radius
    '''
    if hms is None:
        hms = get_time()
    hour, minute, second = hms
    draw_hour_hand(canvas, center, radius, hour, minute)
    draw_minute_hand(canvas, center, radius, minute)
    draw_second_hand(canvas, center, radius, second)