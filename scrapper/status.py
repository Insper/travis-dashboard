import json
import asyncio
import aiohttp
import requests

class Status:

    def __init__(self, url, groups_num):
        self.url = url
        self.groups_num = groups_num
        self.groups = {}
        self.status = {}
        self.format_link()
        self.status = ''

    def get_groups_url(self):
        r = requests.get(self.url)
        data = r.text
        return(data.split("\r\n")[1:]) # retira header

    def format_link(self):
        groups_url = self.get_groups_url()
        for lines in groups_url:
            try:
                a = lines.split(",")
                link = ''
                if(len(a[1]) > 0):
                    link = "https://api.travis-ci.com" + a[1].split("github.com")[1] + ".svg?branch\=master"
                self.groups[a[0]] = {}
                self.groups[a[0]]["link"] = link
            except:
                print("Link not formated correctly")

    def get_status(self):
        self.status = ''
        for group in self.groups:
            url = self.groups[group]['link']
            if len(url) > 0:
                r = requests.get(url)
                self.status += self.parse_svg(r.text)
            else:
                self.status += 'B'

    def parse_svg(self, svg):
        if svg.find('failing') > -1:
            return "R"
        elif svg.find('passing'):
            return "G"
        else:
            return "B"

    def run(self):
        self.get_status()
        print(self.status)
        #self.format_results()
