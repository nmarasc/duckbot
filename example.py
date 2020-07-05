#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import os

from duckbot import Duckbot

def main():
    token = os.getenv('DISCORD_TOKEN')
    duckbot = Duckbot(token)
    duckbot.run()

if __name__ == '__main__':
    main()
