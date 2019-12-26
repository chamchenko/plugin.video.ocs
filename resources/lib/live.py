# -*- coding: utf-8 -*-
import json, xbmcplugin, sys, xbmc
import requests
from vars import *
from tools import log
from create_item import addLink

def getLive():
    log('getLive')
    xbmcplugin.setContent(int(sys.argv[1])    , 'episodes')
    headers     = {'User-Agent': USER_AGENT}
    items       = json.loads(requests.get(LIVES_API, headers=headers).content.decode('utf-8'))['contents']
    for item in items:
        streamID    = item['playinfo']['cid']
        StartTime   = item['startdatetime'].split('T')[1].rsplit('+')[0].rsplit(':',1)[0]
        EndTime     = item['enddatetime'].split('T')[1].rsplit('+')[0].rsplit(':',1)[0]
        title       = "OCS "+item['key'].title()+'\n[%s]'%(item['title'][0]['value'])
        icon        = IMAGE_BURL+item['channelimageurl']
        thumb       = IMAGE_BURL+item['imageurl']
        fanart      = IMAGE_BURL+item['fullscreenimageurl']
        plot        = '%s [%s-%s]:\n%s'%(item['title'][0]['value'],StartTime,EndTime,item['summary'])
        infoLabels  = {"mediatype":"episode", "title":title, "plot":plot, "TVShowTitle":title}
        infoArt     = {"thumb":thumb,"poster":thumb,"fanart":fanart,"icon":icon,"logo":icon}
        addLink(title, streamID, 9, infoLabels, infoArt, len(items))
