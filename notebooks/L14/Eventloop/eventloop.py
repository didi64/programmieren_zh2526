import threading


move = None  # ueberschreibe mit Funktion, die vom Eventloop aufgerufen wird 

stop_event = threading.Event()
event_queue = []


def event_loop(last_event=None, count=0):
    if event_queue:
        key = event_queue.pop()
    else:
        key = last_event

    move(cmd)

    if not stop_event.is_set():
        thread = threading.Timer(1, event_loop, args=(key, count+1))
        thread.name = f'Eventloop-{count}'
        thread.start()