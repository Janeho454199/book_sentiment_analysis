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


class Field(object):
    """
    Field class
    """
    def __init__(self, column_type, value):
        """
        Init Field class
        :param column_type: field type
        """
        self.column_type = column_type
        self.value = value

    def __str__(self):
        return '<%s>' % self.__class__.__name__

    def __set__(self, instance, value):
        if isinstance(value, self.column_type):
            self.value = value
        else:
            raise TypeError("{} must be a {}".format(self.__class__.__name__, self.column_type))

    def __get__(self, instance, owner):
        return self.value


class StringField(Field):
    """
    StringField class
    """
    def __init__(self):
        super(StringField, self).__init__(column_type=str, value='null')


class IntegerField(Field):
    """
    IntegerField class
    """
    def __init__(self):
        super(IntegerField, self).__init__(column_type=int, value=0)


class ItemMeta(type):
    """
    Metaclass for an item
    """

    def __new__(mcs, name, bases, attrs):
        if name == "Item":
            return super().__new__(mcs, name, bases, attrs)
        else:
            table_name = name.lower()
            filed_dic = {}
            for k, v in attrs.items():
                if isinstance(v, Field):
                    filed_dic[k] = v
            attrs["table_name"] = table_name  # 给dic新加一个table_name的属性，将表名添加到dic中，实现类名与表名的映射关系
            attrs["filed_dict"] = filed_dic  # 给dic新加一个filed_dict的属性，将属于BaseFiled类型的属性给添加到dic中，实现属性与字段的映射关系
        return super().__new__(mcs, name, bases, attrs)


class Item(metaclass=ItemMeta):
    """
    Item class for each item
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():  # 遍历传进来的所有属性
            setattr(self, k, v)
