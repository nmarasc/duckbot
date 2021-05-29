# -*- coding: utf-8 -*-
r"""Mongoengine document definitions.

Classes
-------
App
    Steam application entry
"""

from mongoengine import Document
from mongoengine.fields import IntField, StringField


class App(Document):
    appid = IntField(required=True)
    name = StringField(required=True)
