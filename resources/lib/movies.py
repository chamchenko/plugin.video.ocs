# -*- coding: utf-8 -*-
import json, xbmcplugin, sys, xbmc
from web_browser import cacheURL
from vars import *
from ocs_tools import log, getDuration
from create_item import addLink, addDir

def getMovies(url):
    log('getMovies')
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    headers         = {'User-Agent': USER_AGENT}
    items           = json.loads(cacheURL(url,headers))
    for item in items['contents']:
        movieID     = item['id']
        title       = item['title'][0]['value'].lower().title()
        thumb       = IMAGE_BURL+item['imageurl']
        fanart      = thumb.split('?')[0]
        infos       = json.loads(cacheURL(MOVIE_API%movieID,headers))['contents']
        plot        = title+':\n'+infos['summary']
        runtime     = infos['duration']
        duration    = getDuration(runtime)
        streamID    = infos['playinfoid']['sd']
        infoLabels  = {"mediatype":"episode", "title":title, "plot":plot, "TVShowTitle":title}
        infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
        addLink(title, streamID, 9, infoLabels, infoArt, len(items))
    next            = items['next']
    if next:
        nexturl     = API_BURL+next
        infoList    = {"mediatype":"episode", "title":"Next"}
        infoArt     = {"thumb":ICON,"poster":ICON,"fanart":FANART,"icon":ICON,"logo":ICON}
        addDir("Next", nexturl, 5, infoArt, infoList)
