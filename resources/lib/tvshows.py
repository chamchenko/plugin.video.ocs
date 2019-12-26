# -*- coding: utf-8 -*-
import json, xbmcplugin, sys, xbmc
from web_browser import cacheURL
from vars import *
from tools import log, uni
from ocs_tools import getDuration
from create_item import addDir, addLink

def getTvShows(url):
    log('getTvShows')
    xbmcplugin.setContent(int(sys.argv[1])    , 'episodes')
    headers         = {'User-Agent': USER_AGENT}
    items           = json.loads(cacheURL(url,headers))
    for item in items['contents']:
        showId      = item['detaillink'].rsplit('/',1)[1]
        title       = item['title'][0]['value']
        thumb       = IMAGE_BURL+item['imageurl']
        fanart      = thumb.split('?')[0]
        infoList    = {"mediatype":"episode", "title":title, "TVShowTitle":title}
        infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
        addDir(title, showId, 3, infoArt, infoList)
    next            = items['next']
    if next:
        nexturl     = API_BURL+next
        infoList    = {"mediatype":"episode", "title":LANGUAGE(40012)}
        infoArt     = {"thumb":ICON,"poster":ICON,"fanart":FANART,"icon":ICON,"logo":ICON}
        addDir(LANGUAGE(40012), nexturl, 2, infoArt, infoList)

def getSeasons(showId):
    log('getSeasons')
    xbmcplugin.setContent(int(sys.argv[1])    , 'episodes')
    headers         = {'User-Agent': USER_AGENT}
    items           = json.loads(cacheURL(SHOW_API%showId,headers))['contents']
    TVShowTitle     = ""
    for item in items['seasons']:
        seasonID    = item['id']
        plot        = item['pitch']
        thumb       = IMAGE_BURL+item['imageurl']
        fanart      = thumb.split('?')[0]
        seasonNum   = item['number']
        title       = LANGUAGE(40013)+' %s'%seasonNum
        infoList    = {"mediatype":"episode", "title":title,"plot":plot, "TVShowTitle":title}
        infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
        infos       = json.dumps({"showId":showId,"seasonID":seasonID,'seasonNum':seasonNum})
        addDir(title, infos, 4, infoArt, infoList)

def getEpisodes(infos):
    log('getEpisodes')
    xbmcplugin.setContent(int(sys.argv[1])    , 'episodes')
    items       = json.loads(infos)
    showId      = items['showId']
    seasonID    = items['seasonID']
    seasonNum   = items['seasonNum']
    headers     = {'User-Agent': USER_AGENT}
    showjson    = json.loads(cacheURL(SHOW_API%showId,headers))['contents']
    showTitle   = showjson['title'][0]['value']
    seasons     = showjson['seasons']
    for season in seasons:
        if season['id'] != seasonID: continue
        for item in season['episodes']:
            streamID            = item['playinfoid']['sd']        # ['acontents'][0]['contents'][0]['playinfoid']['sd']
            title               = item['title'][0]['value'].title()+':\n'
            plot                = title+':\n'+item['summary']
            thumb               = IMAGE_BURL+item['imageurl']
            fanart              = thumb.split('?')[0]
            episodeNum          = item['number']
            seinfo              = ('S' + ('0' if seasonNum < 10 else '') + str(seasonNum) + 'E' + ('0' if episodeNum < 10 else '') + str(episodeNum))
            runtime             = item['duration']
            duration            = getDuration(runtime)
            infoLabels          = {"mediatype":"episode","title":showTitle+' '+seinfo,"plot":plot,"duration":duration, "TVShowTitle":title}
            infoArt             = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
            addLink(title, streamID, 9, infoLabels, infoArt, len(items))
