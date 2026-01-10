from datetime import datetime

callbacks = {}
event_args = {'new_hour': lambda: (('neue Stunde',) + (d := _get_date())[1][:1], d[0]),
              'new_minute': lambda: (('neue Minute',) + (d := _get_date())[1][:2], d[0]),
              'new_second': lambda: (('neue Sekunde',) + (d := _get_date())[1], d[0]),
              }
events = list(event_args)


def _get_date():
    ds = datetime.today().strftime('%d,%m,%Y,%H,%M,%S').split(',')
    dmy = dict(zip(('Tag', 'Monat', 'Jahr'), ds[:3]))
    hms = tuple(int(x) for x in ds[3:])
    return dmy, hms


def register_callback(event, f):
    assert event in event_args, 'unknown event "{}"'.format(event)
    callbacks[event] = f


def trigger_event(event):
    args, kwargs = event_args[event]()
    if event in callbacks:
        f = callbacks[event]
        f(*args, **kwargs)