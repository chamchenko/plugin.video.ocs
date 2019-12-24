# -*- coding: utf-8 -*-
import json, xbmcplugin, sys, xbmc
from web_browser import cacheURL
from vars import *
from tools import log
from create_item import addLink

def getLive():
    log('getLive')
    xbmcplugin.setContent(int(sys.argv[1])    , 'episodes')
    headers     = {'User-Agent': USER_AGENT}
    items           = json.loads(cacheURL(LIVES_API,headers))['contents']
    for item in items:
        streamID    = item['playinfo']['cid']
        title       = "OCS "+item['key'].title()
        icon        = IMAGE_BURL+item['channelimageurl']
        thumb       = IMAGE_BURL+item['imageurl']
        fanart      = IMAGE_BURL+item['fullscreenimageurl']
        plottitle   = item['title'][0]['value']+':\n'
        plot        = plottitle+item['summary']
        infoLabels  = {"mediatype":"episode", "title":title, "plot":plot, "TVShowTitle":title}
        infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":icon,"logo":icon}
        addLink(title, streamID, 9, infoLabels, infoArt, len(items))
