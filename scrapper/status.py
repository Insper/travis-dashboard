#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import asyncio
import aiohttp
import requests
import collections

class Status:

    def __init__(self, url, groups_num):
        self.url = url
        self.groups_num = groups_num
        self.groups = []
        self.format_link()
        self.status = ''
        self.order = []

    def get_groups_url(self):
        r = requests.get(self.url)
        data = r.text
        return(data.split("\r\n")[1:]) # retira header

    def format_link(self):
        groups_url = self.get_groups_url()
        for lines in groups_url:
            try:
                a = lines.split(",")
                self.groups.append(a[1])
            except:
                print("Link not formated correctly")

    def get_status(self):
        self.status = ''
        for url in self.groups:
#            print(url)
            if len(url) > 0:
                r = requests.get(url)
                self.status += self.parse_svg(r.text)
            else:
                self.status += 'C'

    def parse_svg(self, svg):
        if svg.find('failing') > -1:
            return "R"
        elif svg.find('passing') > -1:
            return "G"
        else:
            return "C"

    def run(self):
        self.get_status()
        print(self.status)
