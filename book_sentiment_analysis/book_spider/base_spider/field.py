#!/usr/bin/env python

from abc import ABC
from lxml import etree
from .exceptions import NothingMatchedError


class BaseField(object):
    """
    BaseField class
    """

    def __init__(self, css_select, xpath_select, default, many):
        """
        Init BaseField class
        url: http://lxml.de/index.html
        :param default: default value
        """
        self.default = default
        self.css_select = css_select
        self.xpath_select = xpath_select
        self.many = many

    def extract(self, *args, **kwargs):
        raise NotImplementedError("Extract is not implemented.")


class _LxmlElementField(BaseField, ABC):
    def __init__(
        self,
        css_select: str = None,
        xpath_select: str = None,
        default=None,
        many: bool = False,
    ):
        """
        :param css_select: css select http://lxml.de/cssselect.html
        :param xpath_select: http://www.w3school.com.cn/xpath/index.asp
        :param default: inherit
        :param many: inherit
        """
        super(_LxmlElementField, self).__init__(css_select=css_select, xpath_select=xpath_select,
                                                default=default, many=many)
        self.css_select = css_select
        self.xpath_select = xpath_select

    def _get_elements(self, *, html_etree: etree._Element):
        if self.css_select:
            elements = html_etree.cssselect(self.css_select)
        elif self.xpath_select:
            elements = html_etree.xpath(self.xpath_select)
        else:
            raise ValueError(
                f"{self.__class__.__name__} field: css_select or xpath_select is expected."
            )
        if not self.many:
            elements = elements[:1]
        return elements

    def _parse_element(self, element):
        raise NotImplementedError

    def extract(self, html_etree: etree._Element, is_source: bool = False):
        elements = self._get_elements(html_etree=html_etree)
        if is_source:
            return elements if self.many else elements[0]

        if elements:
            results = [self._parse_element(element) for element in elements]
        elif self.default is None:
            raise NothingMatchedError(
                f"Extract `{self.css_select or self.xpath_select}` error, "
                "please check selector or set parameter named `default`"
            )
        else:
            results = self.default if type(self.default) == list else [self.default]

        return results if self.many else results[0]


class AttrField(_LxmlElementField):
    """
    This field is used to get attribute.
    """

    def __init__(
        self,
        attr,
        css_select: str = None,
        xpath_select: str = None,
        default="",
        many: bool = False,
    ):
        super(AttrField, self).__init__(
            css_select=css_select, xpath_select=xpath_select, default=default, many=many
        )
        self.attr = attr

    def _parse_element(self, element):
        return element.get(self.attr, self.default)


class ElementField(_LxmlElementField):
    """
    This field is used to get LXML element(s).
    """

    def _parse_element(self, element):
        return element


class TextField(_LxmlElementField):
    """
    This field is used to get text.
    """

    def _parse_element(self, element):
        # Extract text appropriately based on it's type
        if isinstance(element, etree._ElementUnicodeResult):
            strings = [node for node in element]
        else:
            strings = [node for node in element.itertext()]

        string = "".join(strings)
        return string if string else self.default
