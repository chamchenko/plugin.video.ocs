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
        else:
            headers     = {"User-Agent": USER_AGENT}
            request1    = requests.get(API_OPP, headers=headers)
            Response1   = request1.content.decode('utf-8').strip()
            for item in json.loads(Response1):
                if item['name']=="CANAL":
                    authurl = item['authurl']; homeurl=item['homeurl'].rsplit('/',1)[0].replace('http:','https:')
                    break
            request2    = requests.get(authurl, headers=headers, allow_redirects=False)
            cookies2    = request2.cookies.get_dict()
            cookie_abck = cookies2['_abck']
            nextlocation= request2.headers['Location']
            request3    = requests.get(nextlocation, headers=headers, cookies=cookies2, allow_redirects=False)
            cookies3    = request3.cookies.get_dict()
            cookies3.update(cookies2)
            URL         = 'https://compte-canal.canal-plus.com/static/f5e27e009a815462472c3d86c3e6bf9'
            headers4    = {"User-Agent": USER_AGENT, "Referer":nextlocation}
            paload      = '{"sensor_data":"7a74G7m23Vrp0o5c9033361.43-1,2,-94,-100,%s,uaend,12147,20030107,en-US,Gecko,3,0,0,0,388074,5624434,1920,1056,1920,1080,1920,981,1920,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:1,bat:0,x11:0,x12:1,7582,0.745219591372,788617812216.5,loc:-1,2,-94,-101,do_en,dm_en,t_en-1,2,-94,-105,0,-1,0,0,906,829,0;1,-1,0,0,825,748,0;-1,2,-94,-102,0,-1,0,0,906,829,0;1,-1,0,0,825,748,0;-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,%s-1,2,-94,-115,1,1,0,0,0,0,0,123,0,1577235624433,11,16872,0,0,2812,0,0,124,0,0,%s,30657,425,1577600573,30261689-1,2,-94,-106,9,1-1,2,-94,-119,-1-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-70,1181238206;dis;,7,8;true;true;true;-60;true;24;24;true;false;-1-1,2,-94,-80,4947-1,2,-94,-116,703054147-1,2,-94,-118,128394-1,2,-94,-121,;2;6;0"}'%(USER_AGENT,nextlocation,cookie_abck)
            request4    = requests.post(URL, data=paload, headers=headers, cookies=cookies3, allow_redirects=False)
            cookies4    = request4.cookies.get_dict()
            cookies4.update({'JSESSIONID':cookies3['JSESSIONID']})
            data        = {'error':'','ssoEmail':email ,'ssoPass':password, '__checkbox_ssoMem':'true','__checkbox_ssoMem':'true','ssoMem':'true'}
            data        = urllib.urlencode(data)
            headers5    = {"User-Agent": USER_AGENT, "Referer":nextlocation, 'content-type': 'application/x-www-form-urlencoded'}
            request5    = requests.post(nextlocation, data=data, headers=headers5,cookies=cookies4, allow_redirects=False)
            cookies5    = request5.cookies.get_dict()
            try:s_pass_token        = cookies5['s_pass_token']
            except:
                xbmcgui.Dialog().notification(ADDON_NAME, LANGUAGE(40011), ICON, 4000)
                return None
            cookies5.update({'_abck':cookies4['_abck']})
            headers6    = {"User-Agent": USER_AGENT, "Referer":nextlocation}
            request6    = requests.get(authurl, headers=headers6,cookies=cookies5, allow_redirects=False)
            nexturl     = request6.headers['Location']
            nextheader  = {"User-Agent":USER_AGENT, "Referer": "https://www.fransat.fr/"}
            request7    = requests.get(nexturl, headers=nextheader, allow_redirects=False)
            cookiesOAT  = request7.cookies.get_dict()
            nexturl=request7.headers['Location']
            request8    = requests.get(nexturl, headers=nextheader,cookies=cookiesOAT, allow_redirects=False)
            ocsUserAuth = request8.cookies.get_dict()
            return cookiesOAT

def OCS(): return None # to do
def Orange(): return None # to do
def BouyguesTelecom(): return None # to do
def PlayStation(): return None # to do
def SFR(): return None # to do
def Free(): return None # to do
def Molotov(): return None # to do
def TeleclubSwisscom(): return None # to do
def Vialis(): return None # to do
def VIDEOFUTUR(): return None # to do
def OCSWiBox(): return None # to do
def OCSYouboox(): return None # to do
def MonacoTelecom(): return None # to do
def ParaboleReunion(): return None # to do
def Zeop(): return None # to do
def MauritiusTelecom(): return None # to do
def CodePro(): return None # to do
