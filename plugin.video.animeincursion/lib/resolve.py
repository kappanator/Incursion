import xbmcgui
try:
    import resolveurl
except:
    pass

class resolve:

    def resolve(self, link_list):

        for i in link_list:
            try:
                if direct == False:
                    import resolveurl
                    path = resolveurl.resolve(i['url'])
                    break
                else:
                    path = i['url']
                    break
            except:
                continue
        return u