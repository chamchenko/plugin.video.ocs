# -*- coding: utf-8 -*-
#serie ->> seasons
#group/magazine ->> single season
#programm ->> single videos

import json, xbmcplugin, sys, xbmc
from web_browser import cacheURL
from vars import *
from tools import log, uni
from ocs_tools import getDuration, getCookieOAT2
from movies import getMovies
from create_item import addDir, addLink

headers = {'User-Agent': USER_AGENT}

def getMixed(url,name):
    log('getMixed')
    xbmcplugin.setContent(int(sys.argv[1]) , 'episodes')
    if name == LANGUAGE(40009):
        cookiesOAT2 = json.loads(getCookieOAT2())['cookiesOAT2']
        items       = json.loads(cacheURL(url,headers,cookiesOAT2,False))
    else: items     = json.loads(cacheURL(url,headers))
    for item in items['contents']:
        typecontent = item['detaillink'].split('/')[4]
        if typecontent == "programme":
            addVideo(item)
        elif typecontent == "groupe" or typecontent == "magazine":
            addVideosGroup(item)
        elif typecontent == "serie":
            addSeasonsGroup(item)
    next            = items['next']
    if next:
        nexturl     = API_BURL+next
        infoList    = {"mediatype":"episode", "title":LANGUAGE(40012)}
        infoArt     = {"thumb":ICON,"poster":ICON,"fanart":FANART,"icon":ICON,"logo":ICON}
        addDir(LANGUAGE(40012), nexturl, 8, infoArt, infoList)

def addVideo(item):
    log('addVideo')
    url             = API_BURL+item['detaillink']
    infos           = json.loads(cacheURL(url,headers))['contents']
    streamID        = infos['playinfoid']['sd']
    if streamID:
        plot        = infos['summary']
        subtitle    = item['subtitle'].title()
        title       = item['title'][0]['value'].lower().title()+' [%s]'%subtitle
        thumb       = IMAGE_BURL+item['imageurl']
        fanart      = thumb.split('?')[0]
        progID      = infos['id']
        runtime     = infos['duration']
        duration    = getDuration(runtime)
        infoLabels  = {"mediatype":"episode", "title":title, "plot":plot, "duration":duration, "TVShowTitle":title}
        infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
        addLink(title, streamID, 9, infoLabels, infoArt,0,progID)

def addSeasonsGroup(item):
    log('addSeasonsGroup')
    subtitle    = item['subtitle']
    title       = item['title'][0]['value'].lower().title()+' [%s]'%subtitle
    thumb       = IMAGE_BURL+item['imageurl']
    fanart      = thumb.split('?')[0]
    showId      = item['detaillink'].rsplit('/',1)[1]
    infoList    = {"mediatype":"episode", "title":title, "TVShowTitle":title}
    infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
    addDir(title, showId, 3, infoArt, infoList,0,showId)

def addVideosGroup(item):
    log('addVideosGroup')
    subtitle    = item['subtitle']
    title       = item['title'][0]['value'].lower().title()+' [%s]'%subtitle
    thumb       = IMAGE_BURL+item['imageurl']
    fanart      = thumb.split('?')[0]
    url         = API_BURL+item['detaillink']
    groupId     = url.rsplit('/',1)[1]
    infoList    = {"mediatype":"episode", "title":title, "TVShowTitle":title}
    infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
    addDir(title, url, 10, infoArt, infoList,0,groupId)

def getDocsMagsFavs(url):
    log('getDocsMagsFavs')
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    headers             = {'User-Agent': USER_AGENT}
    episodes            = json.loads(cacheURL(url,headers))['contents']['episodes']
    for item in episodes:
        streamID        = item['playinfoid']['sd']        # ['acontents'][0]['contents'][0]['playinfoid']['sd']
        if streamID:
            title       = item['title'][0]['value'].title()+':\n'
            plot        = title+':\n'+item['summary']
            thumb       = IMAGE_BURL+item['imageurl']
            fanart      = thumb.split('?')[0]
            runtime     = item['duration']
            duration    = getDuration(runtime)
            infoLabels  = {"mediatype":"episode","title":title,"plot":plot,"duration":duration, "TVShowTitle":title}
            infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":ICON,"logo":ICON}
            addLink(title, streamID, 9, infoLabels, infoArt, len(episodes))
