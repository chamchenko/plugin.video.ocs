# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import xbmcaddon, json, requests
ADDON_ID        = 'plugin.video.ocs'
REAL_SETTINGS   = xbmcaddon.Addon(id=ADDON_ID)
ADDON_NAME      = REAL_SETTINGS.getAddonInfo('name')
SETTINGS_LOC    = REAL_SETTINGS.getAddonInfo('profile')
ADDON_PATH      = REAL_SETTINGS.getAddonInfo('path')
ADDON_VERSION   = REAL_SETTINGS.getAddonInfo('version')
ICON            = REAL_SETTINGS.getAddonInfo('icon')
FANART          = REAL_SETTINGS.getAddonInfo('fanart')
LANGUAGE        = REAL_SETTINGS.getLocalizedString
PROVIDER        = REAL_SETTINGS.getSetting('provider').strip().replace(' ','').replace('/','')
email           = REAL_SETTINGS.getSetting('username')
password        = REAL_SETTINGS.getSetting('password')
TIMEOUT         = 15
USER_AGENT      = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
DEBUG           = REAL_SETTINGS.getSetting('Enable_Debugging') == 'true'
Hide_Clips      = REAL_SETTINGS.getSetting('Hide_Clips') == 'true'
QUALITY         = REAL_SETTINGS.getSetting('Quality').replace('p','')
MAXBANDWIDTH    = xbmcaddon.Addon(id='inputstream.adaptive').getSetting('MAXBANDWIDTH')
MINBANDWIDTH    = xbmcaddon.Addon(id='inputstream.adaptive').getSetting('MINBANDWIDTH')
STREAMSELECTION = xbmcaddon.Addon(id='inputstream.adaptive').getSetting('STREAMSELECTION')
CONF_URL        = 'https://go.ocs.fr/conf'
CONFS           = json.loads(requests.get(CONF_URL, headers={"User-Agent":USER_AGENT}).content.decode('utf-8'))
BASE_URL        = 'https://go.ocs.fr/'
API_BURL        = CONFS['urlBaseAPI']
API_TargetWeb   = CONFS['apiTargetWeb']
IMAGE_BURL      = CONFS['imageServerUrl']
API_OPP         = API_BURL + API_TargetWeb + 'distributors?ocs_redirect_uri=https%3A%2F%2Fgo.ocs.fr%2F&ocs_state=https%3A%2F%2Fgo.ocs.fr%2F'
LIVES_API       = API_BURL + API_TargetWeb + 'rubriques/live'
MOVIES_API      = API_BURL + API_TargetWeb + 'rubriques/films?limit=22'
MOVIE_API       = API_BURL + API_TargetWeb + 'details/programme/%s'
SHOWS_API       = API_BURL + API_TargetWeb + 'rubriques/series?limit=22'
SHOW_API        = API_BURL + API_TargetWeb + 'details/serie/%s'
DOCS_API        = API_BURL + API_TargetWeb + 'rubriques/documentaires?limit=22'
MAGAZINES_API   = API_BURL + API_TargetWeb + 'rubriques/magazines?limit=22'
HOUSEHOLD_API   = API_BURL + API_TargetWeb + 'households'
PLAYER_API      = API_BURL + '/core/v1/play/webplayer?cid=%s'
SEARCH_API      = API_BURL + API_TargetWeb + 'contents?search=%s&limit=22'
SEARCH_KIDS_API = API_BURL + API_TargetWeb + 'contents?filter=jeunesse&search=%s&limit=22'
KIDS_SUB_MENU   = [(LANGUAGE(40008), API_BURL + API_TargetWeb + "rubriques/jeunesse?filter=seriejeunesse&limit=22", 2),
                   (LANGUAGE(40003), API_BURL + API_TargetWeb + "rubriques/jeunesse?filter=film&limit=22", 5),
                   (LANGUAGE(40007) ,"",            11)]

MAIN_MENU       = [(LANGUAGE(40001), "",            1),
                   (LANGUAGE(40002), SHOWS_API,     2),
                   (LANGUAGE(40003), MOVIES_API,    5),
                   (LANGUAGE(40004), "",            6),
                   (LANGUAGE(40005), DOCS_API,      8),
                   (LANGUAGE(40006), MAGAZINES_API, 8),
                   (LANGUAGE(40007) ,"",            7),
                   (LANGUAGE(40009) ,"",           12)]
