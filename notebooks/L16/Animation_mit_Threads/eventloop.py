import threading


key_buffer = []
key_handler = None
default_action = None
out = None

stop_event = threading.Event()


def start(count=0):
    if out:
        out.append_stdout(f'running Eventloop-{count}')

    if key_buffer:
        key = key_buffer.pop()
        key_handler(key)
    elif default_action:
        default_action()

    if not stop_event.is_set():
        thread = threading.Timer(1, start, args=(count+1,))
        thread.name = f'Eventloop-{count}'
        thread.start()


def my_threads():
    my_threads = [thread for thread in threading.enumerate()
                  if thread.name.startswith('Eventloop')]
    return my_threads