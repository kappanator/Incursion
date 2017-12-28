# -*- coding: utf-8 -*-

'''
    Incursion Add-on
    Copyright (C) 2016 Incursion

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import requests
import sys
from resources.lib.modules import directstream
from bs4 import BeautifulSoup

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domain = 'beetv.to/'
        self.base_link = 'http://beetv.to/'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = tvshowtitle.replace(' ', '-')
        except:
            print("Unexpected error in Beetv Script:", sys.exc_info()[0])
            return url
        return url

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return url
            with requests.Session() as s:
                p = s.get('http://beetv.to/watch-' + url + '-online')
                soup = BeautifulSoup(p.text, 'html.parser')
                season_list = soup.findAll('a')
                for i in season_list:
                    if ('s' + season + "-e" + episode) in i.get('href'):
                        url = i.get('href')
                        url = url.replace("/", '')
            return url
        except:
            print("Unexpected error in Beetv Script: episode", sys.exc_info()[0])
            return url

    def sources(self, url, hostDict, hostprDict):
        sources = []
        url = str(url)
        if not url:
            return sources

        try:
            with requests.Session() as s:
                p = s.get("http://beetv.to/" + url)
                soup = BeautifulSoup(p.text, 'html.parser')
                iframes = soup.findAll('iframe')
                for i in iframes:
                    if 'thevideo' in i.get('src'):
                        sources.append({'source': "thevideo.me", 'quality': 'SD', 'language': "en", 'url': i['src'], 'info': '','direct': False, 'debridonly': False})
                    if 'openload' in i['src']:
                        sources.append({'source': "openload.co", 'quality': 'SD', 'language': "en", 'url': i['src'], 'info': '','direct': False, 'debridonly': False})
                    if 'vshare' in i['src']:
                        sources.append({'source': "vshare.eu", 'quality': 'SD', 'language': "en", 'url': i['src'], 'info': '','direct': False, 'debridonly': False})
            return sources
        except:
            print("Unexpected error in Beetv Script: sources", sys.exc_info()[0])


    def resolve(self, url):
        if 'google' in url:
            return directstream.googlepass(url)
        else:
            return url
