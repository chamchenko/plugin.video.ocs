# -*- coding: utf-8 -*-
from vars import *
from ocs_tools import getCookieOAT2
import requests
cookiesOAT2     = json.loads(getCookieOAT2())['cookiesOAT2']
headers         = {"User-Agent":USER_AGENT, "x-http-method-override": sys.argv[2], "Referer": BASE_URL, "content-type": "application/x-www-form-urlencoded"}
if sys.argv[2] == "PUT":
    data        = json.dumps({"id":sys.argv[1],"creator":"portal"})
    request     = requests.post(ADD_FAV_API%sys.argv[1], data=data, cookies=cookiesOAT2, headers=headers)
elif sys.argv[2] == "DELETE":
    request     = requests.post(ADD_FAV_API%sys.argv[1], cookies=cookiesOAT2, headers=headers)
