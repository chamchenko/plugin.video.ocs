# -*- coding: utf-8 -*-
import urllib, requests, xbmcgui, xbmc, datetime
from vars import *
from tools import log
from simplecache import SimpleCache

cache = SimpleCache()
def cacheURL(url, headers, cookies=None, CACHE=True):
    log('cacheURL, url = ' + str(url))
    try:
        cacheResponse = cache.get(ADDON_NAME + '.openURL, url = %s,headers = %s'%(url,headers))
        if not cacheResponse or CACHE == False:
            request = requests.get(url, headers=headers, cookies=cookies)
            cacheResponse = request.content.decode('utf-8').strip()
            cache.set(ADDON_NAME + '.openURL, url = %s,headers = %s'%(url,headers), cacheResponse, expiration=datetime.timedelta(hours=1))
        return cacheResponse
    except Exception as e:log("openURL Failed! " + str(e), xbmc.LOGERROR)
    xbmcgui.Dialog().notification(ADDON_NAME, LANGUAGE(30001), ICON, 4000)
    return ''
