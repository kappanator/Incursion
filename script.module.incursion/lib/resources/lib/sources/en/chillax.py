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
import json,sys
from resources.lib.modules import control
from resources.lib.modules import directstream
import inspect

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domain = 'chillax.ws'
        self.base_link = 'http://chillax.ws'
        self.search_link = 'http://chillax.ws/search/auto?q='
        self.movie_link = "http://chillax.ws/movies/getMovieLink?"
        self.login_link = 'http://chillax.ws/session/loginajax'
        self.tv_link = 'http://chillax.ws/series/getTvLink?'
        self.login_payload = {'username': '', 'password': ''}

    def movie(self, imdb, title, localtitle, aliases, year):
        with requests.Session() as s:
            try:
                p = s.post(self.login_link, self.login_payload)
                search_text = title
                p = s.get(self.search_link + search_text)
                show_dict = json.loads(p.text)[0]
                url = {'title': search_text, 'id': show_dict['id']}
                p = s.post(self.movie_link + "id=" + url["id"])
                url = json.loads(p.text)
                return url
            except:
                print("Unexpected error in Chillax Script:", sys.exc_info()[0])
                return ""

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = tvshowtitle
            return url
        except:
            print("Unexpected error in Chillax Script:", sys.exc_info()[0])
            return ""

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        with requests.Session() as s:
            try:
                p= s.post(self.login_link, self.login_payload)
                search_text = url
                p = s.get(self.search_link + search_text)
                show_dict = json.loads(p.text)
                for i in show_dict:
                    if i['title'].lower() == search_text.lower():
                        show_dict = i
                        break
                url = {'title': search_text, 'id': show_dict['id'], 'season': season, 'episode': episode}
                link = self.tv_link + "id=%s&s=%s&e=%s" % (url["id"], url['season'], url['episode'])
                p = s.post(link)
                url = json.loads(p.text)
                return url
            except Exception as e:
                print("Unexpected error in Chillax episode Script:")
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(exc_type, exc_tb.tb_lineno)
                return ""

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            source_list = url
            for i in source_list:
                url = self.base_link + i["file"]
                if i['label'] == "360p":
                    i['label'] = "SD"
                sources.append(
                    {'source': "gvideo", 'quality': i['label'], 'language': "en", 'url': url, 'info' : i['type'],
                     'direct': False, 'debridonly': False})
            return sources
        except Exception as e:
            print("Unexpected error in Chillax SOURCE Script:")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)

    def resolve(self, url):
        if 'google' in url:
            return directstream.googlepass(url)
        else:
            return url