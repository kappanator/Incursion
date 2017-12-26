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
from bs4 import BeautifulSoup
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.base_link = 'http://seriescravings.li'
        self.search_link = 'http://seriescravings.li/watch/'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        url = tvshowtitle
        return url

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            with requests.session() as s:
                url = (self.search_link + url.replace(" ", '-')) + \
                      "-season-" + season + "-episode-" + episode + "-" + title.replace(' ', '-')
                print("INFO SERCH URL - " + url)
                p = s.get(url)
                soup = BeautifulSoup(p.text)
                b = soup.findAll('b', {'id': 'ko'})
                urls = []
                for i in b:
                    soup = BeautifulSoup(i['data-iframe'])
                    iframe = soup.find('iframe')
                    urls.append(iframe['src'])
            for i in urls:
                print("INFO - RETURNED URL: " + i)
            return urls
        except:
            print("Unexpected error in SERC episode Script:", sys.exc_info()[0])
            pass

    def sources(self, url, hostDict, hostprDict):
        print("INFO SERC SOURCES ENTERED")
        sources = []
        try:
            print("INFO ENTERING SOURCES LOOP")
            for i in url:
                print("INFO SERC URL" + i)
                if "thevideo" in i:
                    sources.append(
                        {'source': "thevideo.me", 'quality': "SD", 'language': "en", 'url': i, 'info': '',
                         'direct': False, 'debridonly': False})
                elif "vidzi" in i:
                    sources.append(
                        {'source': "vidzi.tv", 'quality': qual, 'language': "en", 'url': i, 'info': '',
                         'direct': False, 'debridonly': False})
                elif "vidto" in i:
                    sources.append(
                        {'source': "vidto.me", 'quality': "SD", 'language': "en", 'url': i, 'info': '',
                         'direct': False, 'debridonly': False})
                elif "vidup.me" in i:
                    sources.append(
                        {'source': "vidup.me", 'quality': "SD", 'language': "en", 'url': i, 'info': '',
                         'direct': False, 'debridonly': False})
                elif "openload" in i:
                    sources.append(
                        {'source': "openload.co", 'quality': "SD", 'language': "en", 'url': i, 'info': '',
                         'direct': False, 'debridonly': False})
            return sources
        except:
            print("Unexpected error in SERC source Script:", sys.exc_info()[0])
            return sources

    def resolve(self, url):
        if 'google' in url:
            return directstream.googlepass(url)
        else:
            return url