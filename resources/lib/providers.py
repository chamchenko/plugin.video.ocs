# -*- coding: utf-8 -*-
import urllib, json, requests, re, datetime, xbmcgui
from bs4 import BeautifulSoup
from vars import *
from create_item import addDir, addLink
from simplecache import SimpleCache
cookiecache = SimpleCache()

def FRANSAT():
    cookiesOAT = cookiecache.get(ADDON_NAME + '.cookiesOAT')
    if not cookiesOAT:
        if email == "" or password == "":
            xbmcgui.Dialog().notification(ADDON_NAME, LANGUAGE(40010), ICON, 4000)
            return None
        else:
            headers     = {"User-Agent": USER_AGENT}
            request1    = requests.get(API_OPP, headers=headers)
            Response1   = request1.content.decode('utf-8').strip()
            for item in json.loads(Response1):
                if item['name']=="FRANSAT":
                    authurl = item['authurl']; homeurl=item['homeurl'].rsplit('/',1)[0].replace('http:','https:')
                    break
            request2    = requests.get(authurl, headers=headers)
            cookies     = request2.cookies.get_dict()
            Response2   = request2.content.decode('utf-8').strip()
            soup        = BeautifulSoup(Response2, "html.parser")
            pathurl     = urllib.unquote(soup('form',{'method':'post'})[0]['action'])
            token       = soup('input',{'name':'ocs_auth[_token]'})[0]['value']
            posturl     = homeurl+pathurl
            headers     = {"User-Agent": USER_AGENT,"Referer": authurl,"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
            data        = {'ocs_auth[email]':email ,'ocs_auth[password]':password, 'ocs_auth[_token]':token}
            data        = urllib.urlencode(data)
            request3    = requests.post(posturl, data=data, headers=headers, cookies=cookies, allow_redirects=False)
            try :nexturl= request3.headers['location']
            except:
                xbmcgui.Dialog().notification(ADDON_NAME, LANGUAGE(40011), ICON, 4000)
                return None
            nextheader  = {"User-Agent":USER_AGENT, "Referer": "https://www.fransat.fr/"}
            request4    = requests.get(nexturl, headers=nextheader, allow_redirects=False)
            nexturl     = request4.headers['Location']
            cookiesOAT  = request4.cookies.get_dict()
            nextheader  = {"User-Agent":USER_AGENT, "Referer": "https://www.fransat.fr/"}
            request5    = requests.get(nexturl, headers=nextheader, cookies=cookiesOAT, allow_redirects=False)
            expire      = request5.headers['set-cookie'].rsplit(';',4)[2]
            ocsUserAuth = request5.cookies.get_dict()
            cookiecache.set(ADDON_NAME + '.cookiesOAT', cookiesOAT, expiration=datetime.timedelta(hours=24))
    return cookiesOAT

def CANAL():
    cookiesOAT = cookiecache.get(ADDON_NAME + '.cookiesOAT')
    if not cookiesOAT:
        if email == "" or password == "":
            xbmcgui.Dialog().notification(ADDON_NAME, LANGUAGE(40010), ICON, 4000)
            return None
        else: pass
            #to do canal auth
