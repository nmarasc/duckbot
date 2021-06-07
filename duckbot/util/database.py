# -*- coding: utf-8 -*-
r"""Mongoengine document definitions.

Classes
-------
App
    Steam application entry

Functions
---------
buildGameDB
    Create the database of Steam games
"""
import logging

from steam.webapi import WebAPI
from mongoengine import Document
from mongoengine.fields import IntField, StringField

logger = logging.getLogger(__name__)


class App(Document):
    appid = IntField(required=True)
    name = StringField(required=True)


def buildGameDB(steamkey):
    r"""Build the database of games.

    Parameters
    ----------
    steamkey
        Steam WebAPI key for fetching game list
    """
    logger.info('Building game database')
    steamAPI = WebAPI(key=steamkey)
    try:
        service = steamAPI.IStoreService
    except AttributeError:
        logger.warning('Steam WebAPI key not provided or service unavailable')
        entry = App(appid=1, name='duck things')
        entry.save()
        return
    response = service.GetAppList(include_games=1, max_results=50000)['response']
    appid = 1
    for app in response['apps']:
        entry = App(appid=appid, name=app['name'])
        entry.save()
        appid += 1
