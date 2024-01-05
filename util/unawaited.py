import asyncio


def unawaited(task, *args, **kwargs):
    return asyncio.ensure_future(task())
