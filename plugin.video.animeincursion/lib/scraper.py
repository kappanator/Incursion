import requests, re, json, sys, urllib


class scraper:
    def __init__(self):
        self.main_link = 'https://www.masterani.me'
        self.poster_link = 'https://cdn.masterani.me/poster/%s'
        self.wallpaper_link = 'https://cdn.masterani.me/wallpaper/0/%s'
        self.episode_thumb_link = 'https://cdn.masterani.me/episodes/%s'
        self.showlist_link = '/api/anime/filter?order=%s&page=%s&type=%s'
        self.detailed_link = '/api/anime/%s/detailed'
        self.genre_link = 'https://www.masterani.me/api/anime/filter?order=score_desc&genres=%s&page=%s&type=%s'
        self.search_link = 'https://www.masterani.me/api/anime/search?search=%s&sb=true'
        self.list = []

    def search(self, url):
        list = []
        url = self.search_link % urllib.quote_plus(url)
        p = requests.get(url)
        p = json.loads(p.text)
        list = self.info_builder(p)

        return list

    def subpagination(self, list, subpage):
        if subpage == 1:
            list = list[:len(list) / 2]
        else:
            list = list[len(list) / 2:]

        return list

    def filterScrape(self, page, type, order, subpage):

        try:
            url = self.main_link + self.showlist_link % (str(order), str(page), str(type))
            p = requests.get(url)
            p = json.loads(p.text)['data']
            list = self.subpagination(p, subpage)
            list = self.info_builder(list)
        except:
            print("Unexpected error in filter scrape script:", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            pass

        return list

    def info_builder(self, array):
        try:
            '''  from multiprocessing.dummy import Pool as ThreadPool

            pool = ThreadPool(2)
            results = pool.map(self.info_builder_thread, array)
            pool.close()
            pool.join()'''

            from lib import workers

            self.list = [] ; threads= []

            for i in array:
                threads.append(workers.Thread(self.info_builder_thread, i))
            [i.start() for i in threads] ; [i.join() for i in threads]


        except:
            print("Unexpected error in info builder script:", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)

        return self.list

    def info_builder_thread(self, i):
        item = {}

        try:
            url = self.main_link + self.detailed_link % str(i['id'])
            details = requests.get(url)
            details = json.loads(details.text)

            item['meta'] = {}
            item['art'] = {}
            item['ids'] = {}
            item['art']['thumb'] = self.poster_link % i['poster']['file']
            item['art']['poster'] = item['art']['thumb']
            try:
                item['art']['fanart'],item['art']['banner'] = self.wallpaper_link % details['wallpapers'][0]['file']
            except:
                pass

            genres = []
            if 'genres' in details:
                for i in details['genres']:
                    genres.append(i['name'])
                item['meta']['genre'] = genres

            item['ids']['tvdb'] = details['info']['tvdb_id']

            if 'started_airing_date' in details['info']:
                item['meta']['year'] = details['info']['started_airing_date'][:4]
            if 'score' in details['info']:
                item['meta']['rating'] = float(details['info']['score']) * 2
            item['meta']['mpaa'] = details['info']['age_rating']
            item['meta']['title'] = details['info']['title']
            item['meta']['plot'] = details['info']['synopsis']
            item['type'] = details['info']['type']
            item['url'] = details['info']['slug']
            item['slug'] = details['info']['slug']
            item['id'] = details['info']['id']

            self.list.append(item)
        except:
            print("Unexpected error in info_builder thread script:", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(str(item))
            print(exc_type, exc_tb.tb_lineno)
            pass

        return

    def episodeList(self, url):
        list = []
        url = (self.main_link + self.detailed_link) % url
        with requests.session() as s:
            p = s.get(url)
            p = json.loads(p.text)
            episodes = p['episodes']
            fanart = self.wallpaper_link % p['wallpapers'][0]['file']

            for i in episodes:
                try:
                    item = {}
                    item['url'] = i['info']['episode']
                    item['type'] = i['info']['type']
                    item['art'] = {}
                    item['art']['thumb'] = self.episode_thumb_link % i['thumbnail']
                    try:
                        item['art']['fanart'] = fanart
                    except:
                        pass

                    item['ids'] = {}
                    item['ids']['tvdb'] = i['info']['tvdb_id']

                    item['meta'] = {}
                    item['meta']['episode'] = i['info']['episode']
                    item['meta']['title'] = i['info']['title']
                    item['meta']['plot'] = i['info']['description'].encode('utf-8')
                    item['meta']['year'] = re.findall(r'....', i['info']['aired'])[0]
                    item['meta']['mediatype'] = 'episode'
                    list.append(item)
                except:
                    print("Unexpected error in episode list script:", sys.exc_info()[0])
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(exc_type, exc_tb.tb_lineno)
                    continue
        return list

    def genreScrape(self, genre_ids, page, subpage, type):
        try:
            genre_string = ''
            for i in genre_ids:
                genre_string += ',' + str(i)

            url = self.genre_link % (genre_string[1:], str(page), str(type))
            p = requests.get(url)
            p = json.loads(p.text)['data']

            list = self.subpagination(p, subpage)
            list = self.info_builder(list)
        except:
            print("Unexpected error in genre scraper script:", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            pass

        return list


    def scrapeLinks(self, slug, url):
        link_list = []
        try:
            list = []
            url = self.main_link + "/anime/watch/%s/%s" % (slug, url)


            with requests.session() as s:
                p = s.get(url)
                print(p.text)
                try:
                    videos = re.findall(r'videos = (\[.*?\])', p.text)[0]
                    videos = json.loads(videos)
                    for i in videos:
                        link_list.append({'url': i['src'],
                                          'name': 'Masteranime',
                                          'quality': i['res'],
                                          'direct':True})
                except:
                    mirrors = re.findall(r'mirrors: (.*?), auto_update', p.text)[0]
                    mirrors = json.loads(mirrors)
                    for i in mirrors:
                        link_list.append({'url': i['host']['embed_prefix'] + i['embed_id'],
                                          'name': i['host']['name'],
                                          'quality': i['quality'],
                                          'direct':False})
        except:

            pass

        return link_list
