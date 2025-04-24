"""
Patch for a NetMRI querying callable that may raise a JSON decode error due to
an apparent NetMRI bug.
"""

class _ext:
    import collections.abc
    import json
    import logging
    import random
    import time
    import typing


logger = _ext.logging.getLogger(__name__)


_TCallable = _ext.typing.TypeVar("_TCallable", bound=_ext.collections.abc.Callable)


class CantRecoverFromNetMRIJsonBug(Exception):
    pass


def json_bug_patch(max_try: int = 5):
    if max_try < 1:
        raise ValueError("max_try must be greater than or equal to 1.")

    def decorator(func: _TCallable) -> _TCallable:
        def wrapped(
            *args: _ext.typing.Any, **kwargs: _ext.typing.Any
        ) -> _ext.typing.Any:
            try_count = 0
            while try_count < max_try:
                try:
                    out = func(*args, **kwargs)
                except _ext.json.decoder.JSONDecodeError as e:
                    if e.args[0] != "Expecting value: line 1 column 1 (char 0)":
                        raise
                    try_count += 1
                    logger.info(
                        "Encountered NetMRI's JSON bug during try #%d.", try_count
                    )
                    # Wait a bit before retrying to give time to system to recover.
                    _ext.time.sleep(_ext.random.randint(0, 5))
                else:
                    return out
            raise CantRecoverFromNetMRIJsonBug

        return wrapped  # type: ignore[return]

    return decorator
