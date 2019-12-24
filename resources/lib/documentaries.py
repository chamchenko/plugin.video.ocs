# -*- coding: utf-8 -*-
#serie ->> seasons
#group/magazine ->> single season
#programm ->> single videos

import json, xbmcplugin, sys, xbmc
from web_browser import cacheURL
from vars import *
from tools import log, uni
from ocs_tools import getDuration
from movies import getMovies
from create_item import addDir, addLink

headers = {'User-Agent': USER_AGENT}

def getDocumentaries(url):
    log('getTvShows')
    xbmcplugin.setContent(int(sys.argv[1])    , 'episodes')
    print 'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU'
    print url
    print 'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU'
    items           = json.loads(cacheURL(url,headers))
    for item in items['contents']:
        typecontent     = item['detaillink'].split('/')[4]
        if typecontent == "programme":
            addVideo(item)
        elif typecontent == "groupe" or typecontent == "magazine":
            addVideosGroup(item)
        elif typecontent == "serie":
            addSeasonsGroup(item)
    next            = items['next']
    if next:
        nexturl     = API_BURL+next
        infoList    = {"mediatype":"episode", "title":"Next"}
        infoArt     = {"thumb":ICON,"poster":ICON,"fanart":FANART,"icon":ICON,"logo":ICON}
        addDir("Next", nexturl, 8, infoArt, infoList)

def addVideo(item):
    subtitle    = item['subtitle'].title()
    title       = item['title'][0]['value'].lower().title()+' [%s]'%subtitle
    thumb       = IMAGE_BURL+item['imageurl']
    fanart      = thumb.split('?')[0]
    url         = API_BURL+item['detaillink']
    infos       = json.loads(cacheURL(url,headers))['contents']
    plot        = infos['summary']
    streamID    = infos['playinfoid']['sd']
    runtime     = infos['duration']
    duration    = getDuration(runtime)
    infoLabels  = {"mediatype":"episode", "title":title, "plot":plot, "duration":duration, "TVShowTitle":title}
    infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
    addLink(title, streamID, 9, infoLabels, infoArt)
def addSeasonsGroup(item):
    subtitle    = item['subtitle']
    title       = item['title'][0]['value'].lower().title()+' [%s]'%subtitle
    thumb       = IMAGE_BURL+item['imageurl']
    fanart      = thumb.split('?')[0]
    showId      = item['detaillink'].rsplit('/',1)[1]
    infoList    = {"mediatype":"episode", "title":title, "TVShowTitle":title}
    infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
    addDir(title, showId, 3, infoArt, infoList)
def addVideosGroup(item):
    subtitle    = item['subtitle']
    title       = item['title'][0]['value'].lower().title()+' [%s]'%subtitle
    thumb       = IMAGE_BURL+item['imageurl']
    fanart      = thumb.split('?')[0]
    seasonId    = item['id']
    infoList    = {"mediatype":"episode", "title":title, "TVShowTitle":title}
    infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
    addDir(title, seasonId, 4, infoArt, infoList)
