#!/usr/bin/env python
"""
-------------------------------------------------
   开发人员：janeho
   开发日期：2022-03-04
   开发工具：PyCharm
   功能描述：
-------------------------------------------------
    Change Activity:

-------------------------------------------------
"""
import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

from functools import wraps


def async_callback(func, **kwargs):
    """
    Call the asynchronous function
    :param func: a async function
    :param kwargs: params
    :return: result
    """
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(func(**kwargs))
    loop.run_until_complete(task)
    return task.result()


def singleton(cls):
    """
    A singleton created by using decorator
    :param cls: cls
    :return: instance
    """
    _instances = {}

    @wraps(cls)
    def instance(*args, **kw):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw)
        return _instances[cls]

    return instance
