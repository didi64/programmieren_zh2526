import threading


callback = None  # Funktion callback(*args), die vom Eventloop aufgerufen wird 

stop_event = threading.Event()
event_queue = []


def event_loop(last_event=None, count=0):
    if event_queue:
        direction = event_queue.pop()
    else:
        direction = last_event

    if direction is not None:
        callback(*direction)

    if not stop_event.is_set():
        thread = threading.Timer(0.3, event_loop, args=(direction, count+1))
        thread.name = f'Eventloop-{count}'
        thread.start()