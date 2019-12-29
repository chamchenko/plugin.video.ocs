# -*- coding: utf-8 -*-
import json, xbmcplugin, sys, xbmc, xbmcgui, urllib
from web_browser import cacheURL
from vars import *
from ocs_tools import getDuration
from tools import log, uni
from create_item import addDir, addLink

def loadSearch(items):
    for item in items['contents']:
        title           = item['title'][0]['value'].lower().title()
        thumb           = IMAGE_BURL+item['imageurl']
        fanart          = thumb.split('?')[0]
        runtime         = item['duration']
        duration        = getDuration(runtime)
        typecontent     = item['detaillink'].split('/')[4]
        if typecontent == 'programme':
            streamID    = item['id']
            infoLabels  = {"mediatype":"episode", "title":title,"duration":duration, "TVShowTitle":title}
            infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
            addLink(title, streamID, 9, infoLabels, infoArt)
        elif typecontent == 'serie':
            showId      = item['detaillink'].rsplit('/',1)[1]
            infoList    = {"mediatype":"episode", "title":title, "TVShowTitle":title}
            infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
            addDir(title, showId, 3, infoArt, infoList)
    next            = items['next']
    if next:
        nexturl     = API_BURL+urllib.quote(items['next'],safe='/')
        infoList    = {"mediatype":"episode", "title":"Next"}
        infoArt     = {"thumb":ICON,"poster":ICON,"fanart":FANART,"icon":ICON,"logo":ICON}
        addDir("Next", nexturl, 6, infoArt, infoList)

def searchContent(url=None):
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    if not url:
        search_string   = xbmcgui.Dialog().input('Search', type=xbmcgui.INPUT_ALPHANUM)
        url             = SEARCH_API%urllib.quote('title='+search_string)
    headers             = {"User-Agent": USER_AGENT}
    items               = json.loads(cacheURL(url,headers))
    try:
        loadSearch(items)
    except:
        xbmcgui.Dialog().notification(ADDON_NAME, LANGUAGE(40014), ICON, 4000)

def searchKidsContent(url=None):
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    if not url:
        search_string   = xbmcgui.Dialog().input('Search', type=xbmcgui.INPUT_ALPHANUM)
        url             = SEARCH_KIDS_API%urllib.quote('title='+search_string)
    headers             = {"User-Agent": USER_AGENT}
    items               = json.loads(cacheURL(url,headers))
    try:
        loadSearch(items)
    except:
        xbmcgui.Dialog().notification(ADDON_NAME, LANGUAGE(40014), ICON, 4000)
