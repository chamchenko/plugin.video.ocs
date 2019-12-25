#   Copyright (C) 2019 CHAMCHENKO
#
#
# This file is part of OCS.
#
# OCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OCS.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

import sys, time, datetime, re, traceback, ast, re
import urlparse, urllib, urllib2, socket, json, HTMLParser
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from tools import *
from live import getLive
from tvshows import getTvShows, getSeasons, getEpisodes
from movies import getMovies
from documentaries import getDocumentaries
from search import searchContent
from ocs_tools import getCookieOAT2
from create_item import addDir
from vars import *
from web_browser import *


socket.setdefaulttimeout(TIMEOUT)
class OCS(object):
    def __init__(self):
        log('__init__')

    def buildMenu(self, items):
        for item in items: addDir(*item)
    def browseLive(self):
        getLive()
    def browseShows(self,url):
        getTvShows(url)
    def browseSeasons(self,showId):
        getSeasons(showId)
    def browseEpisodes(self,infos):
        getEpisodes(infos)
    def browseMovies(self,url):
        getMovies(url)
    def browseSubMenu(self):
        #if name == "Kids": items = KIDS_SUB_MENU
        for item in KIDS_SUB_MENU: addDir(*item)
    def browseDocumentaries(self,url):
        getDocumentaries(url)
    def browseSearch(self,url):
        searchContent(url)
    def playVideo(self, name, streamID, liz=None):
        log('playVideo')
        playerURL       = PLAYER_API%streamID
        cookiesOAT2     = getCookieOAT2()
        if not cookiesOAT2:
            xbmc.executebuiltin('Action(Back)')
        else:
            headersPlayer   = {"User-Agent":USER_AGENT, "Referer": BASE_URL}
            request8        = requests.get(playerURL, headers=headersPlayer, cookies=cookiesOAT2, allow_redirects=False)
            contentPlayer   = request8.content.decode('utf-8').strip()
            patternkey      = "(\'com\.widevine\.alpha\'\:\ \')(http.*)\'"
            patternmanifest = "(player\.load\(\')(http.*)\'"
            keyURL          = re.findall(patternkey,contentPlayer)[0][1]
            playbackURL     = re.findall(patternmanifest,contentPlayer)[0][1]
            liz             = xbmcgui.ListItem(name, path=playbackURL)
            URL_LICENCE_KEY = '%s|User-Agent=%s&referer=%s|R{SSM}|'%(keyURL,USER_AGENT,BASE_URL)
#                                                         [b/B/R]{SSM} and [b/B/R]{SID}  
            liz.setProperty('inputstreamaddon','inputstream.adaptive')
            liz.setProperty('inputstream.adaptive.manifest_type', 'mpd')
            liz.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
            liz.setProperty('inputstream.adaptive.license_key', URL_LICENCE_KEY)
            reqtoken        = requests.get('https://api.ocs.fr/web/v1/streaming', headers=headersPlayer, cookies=cookiesOAT2, allow_redirects=False)
            token           = json.loads(reqtoken.content.decode('utf-8').strip())['token']
            reqdelay        = requests.get('https://api.ocs.fr/web/v1/streaming?token=%s'%token, headers=headersPlayer, cookies=cookiesOAT2, allow_redirects=False)
            delay           = json.loads(reqdelay.content.decode('utf-8').strip())['delay']
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=liz)

params=getParams()
try: url=urllib.unquote_plus(params["url"])
except: url=None
try: name=urllib.unquote_plus(params["name"])
except: name=None
try: mode=int(params["mode"])
except: mode=None
log("Mode: "+str(mode))
log("URL : "+str(url))
log("Name: "+str(name))


if  mode==None: OCS().buildMenu(MAIN_MENU)
elif mode == 1: OCS().browseLive()
elif mode == 2: OCS().browseShows(url)
elif mode == 3: OCS().browseSeasons(url)
elif mode == 4: OCS().browseEpisodes(url)
elif mode == 5: OCS().browseMovies(url)
elif mode == 6: OCS().browseSubMenu()
elif mode == 7: OCS().browseSearch(url)
elif mode == 8: OCS().browseDocumentaries(url)
elif mode == 9: OCS().playVideo(name, url)


xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_UNSORTED)
xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_EPISODE)
xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_DATE)
xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_NONE)
xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_LABEL)
xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_TITLE)
xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
