def make_instance(cls, *args, **kwargs):
    d = {'__class__': cls}

    __init__ = cls.get('__init__')
    if __init__:
        __init__(d, *args, **kwargs)

    return d


def get_attr(instance, attr):
    assert '__class__' in instance, 'did not get an instance of a class'

    if attr in instance:
        return instance[attr]

    elif attr in instance['__class__']:
        obj = instance['__class__'][attr]
        if not callable(obj):
            return obj
        else:
            return lambda *args, **kwargs: obj(instance, *args, **kwargs)

    else:
        cls = instance['__class__']
        raise AttributeError(f"type object '{cls['__name__']}' has no attribute '{attr}'")