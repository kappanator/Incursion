# -*- coding: utf-8 -*-

'''
    Cartoon Incursion Add-on

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

import sys, os
from urlparse import parse_qsl
import xbmcaddon
import xbmc

from lib.navigator import navigator, player

'''###################################################'''
sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])

params = dict(parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')
url = params.get('url')
slug = params.get('slug')
page = params.get('page')
type = params.get('type')
page = params.get('page')
order = params.get('order')
subpage = params.get('subpage')
genres = params.get('genres')

if page is None:
    page = 1

if subpage is None:
    subpage = 1


'''####################################################'''

if action == None:
    navigator().home()

elif action == "showList":
    navigator().showList(page, type, subpage, order=order)

elif action == "episodeList":
    navigator().episodeList(url, slug)

elif action == "tvShows":
    navigator().tvShows()

elif action == "ovaShows":
    navigator().ova()

elif action == "onaShows":
    navigator().ona()

elif action == "specialShows":
    navigator().specials()

elif action == "movies":
    navigator().movies()

elif action == "playItem":
    player().playItem(slug, url)

elif action == "search":
    navigator().search()

elif action == 'genreSearch':
    navigator().genre(page, subpage, genres, type)

elif action == 'tools':
    navigator().tools()

elif action == 'clearCache':
    navigator().clearCache()

elif action == 'searchNew':
    navigator().searchNew()

elif action == 'searchOld':
    query = params.get('query')
    navigator().searchOld(query)

elif action == 'clearSearch':
    navigator().clearSearch()