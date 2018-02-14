from sqlalchemy.engine import url
from sqlalchemy import util

from .engine import GinoEngine


async def create_engine(name_or_url, **kwargs):
    u = url.make_url(name_or_url)

    dialect_cls = u.get_dialect()

    pop_kwarg = kwargs.pop

    dialect_args = {}
    # consume dialect arguments from kwargs
    for k in util.get_cls_kwargs(dialect_cls):
        if k in kwargs:
            dialect_args[k] = pop_kwarg(k)
    dialect = dialect_cls(**dialect_args)

    engine_args = {}
    for k in util.get_cls_kwargs(GinoEngine):
        if k in kwargs:
            engine_args[k] = pop_kwarg(k)

    # all kwargs should be consumed
    if kwargs:
        raise TypeError(
            "Invalid argument(s) %s sent to create_engine(), "
            "using configuration %s/%s.  Please check that the "
            "keyword arguments are appropriate for this combination "
            "of components." % (','.join("'%s'" % k for k in kwargs),
                                dialect_cls.__name__,
                                GinoEngine.__name__))

    engine = GinoEngine(dialect, **engine_args)

    dialect_cls.engine_created(engine)

    return engine
