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


class IgnoreThisItem(Exception):
    """Ignore Ruia's Item"""

    pass


class InvalidCallbackResult(Exception):
    """Get an invalid callback result"""

    pass


class InvalidFuncType(Exception):
    """Get an invalid function result"""

    pass


class NothingMatchedError(Exception):
    """Get an Nothing matched result"""

    pass


class FakeUserAgentError(Exception):
    """Get an FakeUserAgent error"""

    pass
