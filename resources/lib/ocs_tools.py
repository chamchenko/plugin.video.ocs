# -*- coding: utf-8 -*-
import requests, re, json, datetime
import providers
from vars import *
from simplecache import SimpleCache
from tools import log
cookiecache = SimpleCache()
provider    =   {"OCS": providers.OCS, "CANAL": providers.CANAL, "Orange": providers.Orange,
                "BouyguesTelecom": providers.BouyguesTelecom, "PlayStation": providers.PlayStation,
                "SFR": providers.SFR, "Free": providers.Free, "Molotov": providers.Molotov,
                "TeleclubSwisscom": providers.TeleclubSwisscom, "FRANSAT": providers.FRANSAT,
                "Vialis": providers.Vialis, "VIDEOFUTUR": providers.VIDEOFUTUR, "OCSWiBox": providers.OCSWiBox,
                "OCSYouboox": providers.OCSYouboox, "MonacoTelecom": providers.MonacoTelecom,
                "ParaboleReunion": providers.ParaboleReunion, "Zeop": providers.Zeop,
                "MauritiusTelecom": providers.MauritiusTelecom, "CodePro": providers.CodePro}
def getUserID():
    userID = cookiecache.get(ADDON_NAME + '.userID')
    if not userID:
        cookiesOAT  = provider[PROVIDER]()
        if not cookiesOAT:
            userID     = None
        else:
            urluserID   = HOUSEHOLD_API
            headerUI    = {"User-Agent":USER_AGENT, "Referer": "referer: https://go.ocs.fr/"}
            request6    = requests.get(urluserID, headers=headerUI, cookies=cookiesOAT, allow_redirects=False)
            userID      = json.loads(request6.content.decode('utf-8').strip())[0]['id']
            cookiecache.set(ADDON_NAME + '.userID', userID, expiration=datetime.timedelta(hours=24))
    return userID

def getCookieOAT2():
    cookiesOAT2 = cookiecache.get(ADDON_NAME + '.cookiesOAT2')
    if not cookiesOAT2:
        cookiesOAT  = provider[PROVIDER]()
        if not cookiesOAT:
            cookiesOAT2     = None
        else:
            userID          = getUserID()
            urlgetCookie    = HOUSEHOLD_API + '?userid=%s'%userID
            headerGC        = {"User-Agent":USER_AGENT, "Referer": BASE_URL+"profile/select"}
            request7        = requests.get(urlgetCookie, headers=headerGC, cookies=cookiesOAT, allow_redirects=False)
            cookiesOAT2     = request7.cookies.get_dict()
            cookiecache.set(ADDON_NAME + '.cookiesOAT2', cookiesOAT2, expiration=datetime.timedelta(hours=24))
    return cookiesOAT2

def getDuration(runtime):
    try: durationH      = int(runtime.replace('PT','').split('H')[0])*3600
    except:durationH    = 0
    try: durationM      = int(runtime.replace('PT','').split('H')[1].split('M')[0])*60
    except:
        try: durationM  = int(runtime.replace('PT','').split('M')[0])*60
        except:durationM= 0
    try: durationS      = int(runtime.replace('PT','').split('M')[1].split('S')[0])
    except:
        try: durationS  = int(runtime.replace('PT','').split('S')[0])
        except:durationS= 0
    duration            = durationH + durationM + durationS
    return duration
