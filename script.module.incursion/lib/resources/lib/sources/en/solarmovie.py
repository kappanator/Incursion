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
from resources.lib.modules import directstream
from bs4 import BeautifulSoup
import re

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domain = 'solarmoviez.ru'
        self.base_link = 'https://solarmoviez.ru'
        self.search_link = 'https://solarmoviez.ru/ajax/movie_suggest_search.html'
        self.episode_search_link = 'https://solarmoviez.ru/ajax/v4_movie_episodes/'
        self.sources_link = "https://solarmoviez.ru/ajax/movie_sources/"
        self.headers = {'Referer': "https://solarmoviez.ru",
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
        self.data = {'keyword': ''}

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        url={'tvshowtitle': tvshowtitle}
        return url

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            show_title = url['tvshowtitle']
            self.data['keyword'] = show_title + " " + season
            season_link = ""
            sources = []
            if len(episode) == 1:
                episode = "0" + episode
            with requests.Session() as s:
                p = s.post(self.search_link, headers=self.headers, data=self.data)
                search_res = json.loads(p.text)
                search_links = BeautifulSoup(search_res['content'],'html.parser').findAll('a', href=True)
                for i in search_links:
                    if (show_title + " - Season " + season) in i.text:
                        season_link = i['href']
                p = s.get(season_link)
                season_page = BeautifulSoup(p.text,'html.parser')
                for i in season_page.findAll('script', src=False, type=True)[1].prettify().split('\n'):
                    if "id:" in i:
                        season_id = re.sub("[^0-9]", "", i)
                p = s.get(self.episode_search_link + "/" + season_id)
                print(p.text)
                episode_list = BeautifulSoup(json.loads(p.text)['html'], 'html.parser').findAll('li')
                episode_id = []
                for i in episode_list:
                    if ("Episode" + episode) in i.text:
                        episode_id.append((i['data-id']))
                    if ("Episode " + episode) in i.text:
                        episode_id.append((i['data-id']))
            url = {'season_id':season_id,'episode_id':episode_id}
            return url

        except:
            print("Unexpected error in Solarmovie Episode Script:")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
        return ""

    def sources(self, url, hostDict, hostprDict):
        sources = []
        final_links = []
        try:
            episode_id = url['episode_id']
            season_id = url['season_id']
            with requests.Session() as s:
                for i in episode_id:
                    url = "https://solarmoviez.ru/ajax/movie_token?eid=" + i + "&mid=" + season_id
                    p = s.get(url)
                    coord = p.text.replace(" ", '').replace("_", '').replace(";", '').replace("'", '').split(",")
                    url = self.sources_link + i + "?" + coord[0] + "&" + coord[1]
                    p = s.get(url, headers=self.headers)
                    try:
                        source_link = json.loads(p.text)
                        try:
                            if source_link['playlist'][0]['sources'][0]['file']:
                                final_links.append(source_link['playlist'][0]['sources'][0]['file'])
                        except:
                            pass
                        try:
                            if source_link['playlist'][0]['sources']['file']:
                                final_links.append(source_link['playlist'][0]['sources']['file'])
                        except:
                            pass
                    except:
                        print("Unexpected error in Solarmovie episode Script:")
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        print(exc_type, exc_tb.tb_lineno)
                for i in final_links:
                    if 'lemonstream' in i:
                        sources.append(
                            {'source': "lemonstream", 'quality': "720p", 'language': "en", 'url': i+"|Referer="+ self.headers['Referer'], 'info': "",
                             'direct': False, 'debridonly': False})
            return sources
        except:
            print("Unexpected error in Solarmovie Sources Script:")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            pass


    def resolve(self, url):
        if 'google' in url:
            return directstream.googlepass(url)
        else:
            return url
