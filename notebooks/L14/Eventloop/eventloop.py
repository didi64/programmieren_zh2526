import threading
import game


key_move = {'ArrowUp': (0, -1),
            'ArrowDown': (0, 1),
            'ArrowLeft': (-1, 0),
            'ArrowRight': (1, 0),
            }

stop_event = threading.Event()
event_queue = []


def event_loop(last_event=None, count=0):
    if event_queue:
        key = event_queue.pop()
    else:
        key = last_event

    if key in key_move:
        dx, dy = key_move[key]
        game.move(dx, dy)

    if not stop_event.is_set():
        thread = threading.Timer(0.2, event_loop, args=(key, count+1))
        thread.name = f'Eventloop-{count}'
        thread.start()
