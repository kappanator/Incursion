import xbmcgui, xbmcplugin, xbmc, sys, json
from lib.scraper import scraper
from lib import cache
from lib import control

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])

addItem = xbmcplugin.addDirectoryItem
directory = xbmcplugin.endOfDirectory

class navigator:

    def __init__(self):
        self.listing = []

    def home(self):

        self.addDirectoryItem("Movies", "movies")
        self.addDirectoryItem("TV Shows","tvShows")
        self.addDirectoryItem("Original Video","ovaShows")
        self.addDirectoryItem("Original Network","onaShows")
        self.addDirectoryItem("Specials", "specialShows")
        self.addDirectoryItem("Title Search", "search")
        self.addDirectoryItem('Tools', 'tools')
        self.createDirectory(sort=False)

    def movies(self):

        self.addDirectoryItem('All Movies', 'showList', type='2', order='title')
        self.addDirectoryItem("Highest Rated", 'showList', type='2', order='score_desc')
        self.addDirectoryItem('Genre Search', 'genreSearch', type='2')
        self.createDirectory(sort=False)


    def ova(self):

        self.addDirectoryItem('All OVA', 'showList', type='1', order='title')
        self.addDirectoryItem("Highest Rated", 'showList', type='1', order='score_desc')
        self.addDirectoryItem('Genre Search', 'genreSearch', type='1')
        self.createDirectory(sort=False)

    def ona(self):

        self.addDirectoryItem('All ONA', 'showList', type='4', order='title')
        self.addDirectoryItem("Highest Rated", 'showList', type='4', order='score_desc')
        self.addDirectoryItem('Genre Search', 'genreSearch', type='4')
        self.createDirectory(sort=False)

    def specials(self):

        self.addDirectoryItem('All Specials', 'showList', type='3', order='title')
        self.addDirectoryItem("Highest Rated", 'showList', type='3', order='score_desc')
        self.addDirectoryItem('Genre Search', 'genreSearch', type='3')
        self.createDirectory(sort=False)

    def tvShows(self):

        self.addDirectoryItem('All Shows', 'showList', type='0', order='title')
        self.addDirectoryItem("Highest Rated", 'showList', type='0', order='score_desc')
        self.addDirectoryItem('Genre Search', 'genreSearch', type='0')
        self.createDirectory(sort=False)

    def tools(self):
        self.addDirectoryItem('Clear Search History', 'clearSearch', is_folder=False)
        self.addDirectoryItem("Clear Cache", 'clearCache', is_folder=False)
        self.createDirectory(sort=False)

    def subpagination(self, subpage, page):

        subpage = int(subpage)
        page = int(page)
        if subpage == 1:
            subpage += 1
        else:
            subpage = 1
            page += 1
        return subpage, page


    def showList(self, page, type, subpage, order='score_desc'):

        list = cache.get(scraper().filterScrape, 24, page, type, order, subpage)

        subpage, page = self.subpagination(subpage, page)

        self.list_builder(list)

        self.addDirectoryItem('Next', 'showList', page=page, type=type, order=order, subpage=subpage)

        self.createDirectory(sort=False)

    def episodeList(self, url, slug):

        list = cache.get(scraper().episodeList, 24, url)

        for item in list:
            self.addDirectoryItem(item['meta']['title'], "playItem", url=item['url'],
                                  type=item['type'], slug=slug, is_folder=False, playable=True, meta=item['meta'],
                                  art=item['art'])
        self.createDirectory(sort=False)

    def genre(self, page, subpage, genres, type):

        genre_ids = [58,69,57,59,84,86,60,79,77,93,89,82,71,66,95,88,75,85,83,
                     90,63,94,72,73,67,87,78,61,70,91,92,64,96,68,62,65,76,80,74,81,98,97]

        genre_titles = ['Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Drama', 'Ecchi', 'Fantasy',
                        'Game', 'Harem', 'Historical', 'Horror', 'Josei', 'Kids', 'Magic', 'Martial Arts', 'Mecha',
                        'Military', 'Music', 'Mystery', 'Parody', 'Police', 'Psychological', 'Romance', 'Samurai',
                        'School', 'Sci-Fi', 'Seinen', 'Shoujo', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Slice of Life',
                        'Space', 'Sports', 'Super Power', 'Supernatural', 'Thriller', 'Vampire', 'Yaoi', 'Yuri']

        if genres is None:
            genres = xbmcgui.Dialog().multiselect("Genre", genre_titles)
        else:
            genres = json.loads(genres)

        list = []
        for i in genres:
            list.append(genre_ids[int(i)])

        list = cache.get(scraper().genreScrape, 24, list, page, subpage, type)

        subpage, page = self.subpagination(subpage, page)

        self.list_builder(list)

        self.addDirectoryItem('Next', 'genreSearch', page=page, genres=genres, subpage=subpage, type=type)

        self.createDirectory(sort=False)

    def searchNew(self):

        control.busy()

        t = control.lang(32010).encode('utf-8')
        k = control.keyboard('', t);
        k.doModal()
        q = k.getText()

        if (q == None or q == ''): return

        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        dbcur.execute("INSERT INTO search VALUES (?,?)", (None, q))
        dbcon.commit()
        dbcur.close()

        list = cache.get(scraper().search, 24, q)

        self.list_builder(list)

        control.idle()

        self.createDirectory(sort=False)

    def searchOld(self, q):

        list = cache.get(scraper().search, 24, q)

        self.list_builder(list)

        self.createDirectory(sort=False)

        return

    def search(self):

        self.addDirectoryItem('New Search', 'searchNew')
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()

        try:
            dbcur.executescript("CREATE TABLE IF NOT EXISTS search (ID Integer PRIMARY KEY AUTOINCREMENT, term);")
        except:
            pass

        dbcur.execute("SELECT * FROM search ORDER BY ID DESC")

        lst = []

        delete_option = False
        for (id, term) in dbcur.fetchall():
            if term not in str(lst):
                delete_option = True
                self.addDirectoryItem(term, 'searchOld&query=%s' % term)
                lst += [(term)]
        dbcur.close()

        if delete_option:
            self.addDirectoryItem('Clear Search', 'clearSearch', is_folder=False)

        self.createDirectory(sort=False)

    def clearSearch(self):

        confirm = xbmcgui.Dialog().yesno("Anime Incursion", "Clear Search History?")
        if confirm == True:
            cache.cache_clear_search()
            dialog = xbmcgui.Dialog()
            dialog.notification('Anime Incursion', 'Search History Cleared', xbmcgui.NOTIFICATION_INFO, 5000)

    def clearCache(self):
        confirm = xbmcgui.Dialog().yesno("Anime Incursion", "Clear Cache?")
        if confirm == True:
            from lib import cache
            cache.cache_clear_all()
            dialog = xbmcgui.Dialog()
            dialog.notification('Anime Incursion', 'Cleared Cache', xbmcgui.NOTIFICATION_INFO, 5000)

    def list_builder(self, list):

        for item in list:
            try:
                if item['type'] == 2:
                    self.addDirectoryItem(item['meta']['title'], "playItem", url='1',
                                          slug=item['slug'], playable=True, is_folder=False, art=item['art'],
                                          meta=item['meta'])

                elif item['type'] in [0,4,3,1]:
                    self.addDirectoryItem(item['meta']['title'], "episodeList", url=item['id'], slug=item['slug'],
                                          is_folder=True,
                                          art=item['art'], meta=item['meta'])
            except:
                print("Unexpected error in listbuilder script:", sys.exc_info()[0])
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(item))
                print(exc_type, exc_tb.tb_lineno)
                continue

    def addDirectoryItem(self, name, action, url=None, type=None, playable=False, slug=None,
                         is_folder=True, page=1, order=None, meta=None,
                         art=None, subpage=None, genres=None):

        list_item = xbmcgui.ListItem(label=name.encode('utf-8'))
        list_item.setInfo(type='Video', infoLabels=meta)

        if playable == True:
            list_item.setProperty('IsPlayable', 'true')
            list_item.addStreamInfo('video', {'title': name})
            is_folder = False

        if not art is None:
            list_item.setArt(art)

        link = '%s?action=%s' % (sysaddon, action)
        if not genres == None:
            link += "&genres=%s" % str(genres)
        if not subpage == None:
            link += "&subpage=%s" % subpage
        if not order == None:
            link += "&order=%s" % order
        if not type == None:
            link += "&type=%s" % type
        if not url == None:
            link += "&url=%s" % url
        if not slug == None:
            link += "&slug=%s" % slug
        if not page == 1:
            link += "&page=%s" % str(page)

        self.listing.append((link, list_item, is_folder))

    def createDirectory(self, sort=True):

        if sort == True:
            xbmcplugin.addSortMethod(syshandle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)

        xbmcplugin.addDirectoryItems(syshandle, self.listing, len(self.listing))
        xbmcplugin.endOfDirectory(syshandle)


class player:

    def playItem(self, slug, url):
        control.busy()
        resolve_dialog = xbmcgui.DialogProgress()
        link_list = cache.get(scraper().scrapeLinks, 24, slug, url)
        control.idle()

        if len(link_list) == 0:

            dialog = xbmcgui.Dialog()
            dialog.notification('Anime Incursion', 'No Links Available', xbmcgui.NOTIFICATION_INFO, 5000)

        else:

            resolve_dialog.create('Anime Incursion', '')
            resolve_dialog.update(0)
            link_list = sorted(link_list, key=lambda x: (x['quality']), reverse=True)
            link_total = len(link_list)
            progress = 0
            path = ''

            for i in link_list:
                # if resolve_dialog.iscanceled() == True:
                #   return

                progress += 1
                resolve_dialog.update(int((100 / float(link_total)) * progress), str(progress) + ' | [B]Host: ' +
                                      i['name'].upper() + "[/B] | [B]Resolution: " +
                                      str(i['quality']) + "p[/B]")
                try:
                    if i['direct'] == False:

                        import resolveurl
                        path = resolveurl.resolve(i['url']).encode('utf-8')
                        break
                    else:
                        path = i['url']
                        break
                except:
                    continue

            if path != '':
                play_item = xbmcgui.ListItem(path=path)
                print('INFO - ' + str(sys.argv[1]))
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=play_item)
            else:
                dialog = xbmcgui.Dialog()
                dialog.notification('Anime Incursion', 'Unable to Resolve Links', xbmcgui.NOTIFICATION_INFO, 5000)