def get_centers(x, y, r):
    pts = [(x, y - 2*r),  # 1
           (x, y - r),    # 2
           (x + r, y),    # 3
           (x, y + r),    # 4
           (x-r, y),      # 5
           ]
    return pts


def draw_bg(canvas, x, y, r):
    canvas.clear()
    canvas.fill_text('Schiebespiel', 20, 20)
    canvas.stroke_style = 'blue'
    canvas.stroke_circle(x, y, r)
    canvas.stroke_style = 'red'

    pts = get_centers(x, y, r)
    canvas.stroke_lines([pts[0], pts[1]])
    canvas.stroke_lines([pts[2], pts[4]])

    canvas.stroke_style = 'black'
    r1 = 10
    for x, y in pts:
        canvas.clear_rect(x-r1, y-r1, 2*r1)
        canvas.stroke_circle(x, y, r1)


def update_scramble(canvas, state, pts):
    canvas.clear()
    for i, n in enumerate(state):
        x, y = pts[i]
        canvas.fill_text(str(n), x, y)


def distance(v, w):
    return max(abs(w[0]-v[0]), abs(w[1]-v[1]))


def get_nearest_pt(point, points):
    '''gibt Abstand und Index des naechsten Punktes in points zurueck'''
    return min((distance(point, pt), i) for i, pt in enumerate(points))


def get_nearest_idx(pt, points, err=10):
    '''gibt Index des naechsten Punktes zurueck, falls naeher als err'''
    dist, idx = get_nearest_pt(pt, points)
    if dist < err:
        return idx
