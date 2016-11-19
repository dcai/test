#!/usr/bin/env python3
# -- coding: utf-8 --

import logging.config
import requests
import time
import configparser
import os,sys
from bs4 import BeautifulSoup

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client

#http_client.HTTPConnection.debuglevel = 1

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'

cfg = configparser.ConfigParser()
dirname=os.path.dirname(os.path.realpath(sys.argv[0]))
cfg.read("{}/credentials.ini".format(dirname))

l = logging.getLogger('checkin')
l.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create file handler which logs even debug messages
fileHandler = logging.FileHandler('/tmp/test.log')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
l.addHandler(fileHandler)

# create console handler with a higher log level
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.ERROR)
streamHandler.setFormatter(formatter)
l.addHandler(streamHandler)

def checkin_netease(music_u, csrf):
    TYPE_WEBPC = 1
    TYPE_ANDROID = 0
    cookies = {
        'MUSIC_U': music_u,
        '__remember_me': 'true',
        '__csrf': csrf
    }
    headers = {
        'User-Agent' : UA,
        'Referer': 'http://music.163.com/'
    }
    # web & pc
    url = 'http://music.163.com/api/point/dailyTask?type={}'.format(TYPE_WEBPC)
    response = requests.post(url, cookies=cookies, headers=headers)
    wjson = response.json()
    log_from_code(wjson, 'netease: web & pc')
    # android
    url = 'http://music.163.com/api/point/dailyTask?type={}'.format(TYPE_ANDROID)
    response = requests.post(url, cookies=cookies, headers=headers)
    ajson = response.json()
    log_from_code(ajson, 'netease: android')

def log_from_code(response_json, platform):
    code = response_json['code']
    if code == -2:
        l.info('{}: you already checked in today.'.format(platform))
    elif code == 200:
        l.info('{} OK. +{} points'.format(platform, response_json['point']))
    else:
        l.info('{} failed. {}({})'.format(platform, code, response_json['msg']))

def checkin_zimuzu(username, password):
    backurl = 'http://www.zimuzu.tv/user/sign'
    data = {
        'account': username,
        'password': password,
        'remember': 1,
        'url_back': backurl
    }
    headers = {
        'User-Agent' : UA,
        'Referer': 'http://www.zimuzu.tv'
    }
    r = requests.post("http://www.zimuzu.tv/User/Login/ajaxLogin", data = data, headers=headers)
    try:
        o = r.json()
        l.info('zimuzu: {}'.format(o['info']))
    except Exception as e:
        l.info(e)
        pass

    #url = "http://www.zimuzu.tv/user/login/getCurUserTopInfo"
    #r1 = requests.get(url, cookies=r.cookies, headers=headers)
    ##l.info(r1.json())

    ## open checkin page and wait 16 seconds
    #r2 = requests.get(backurl, cookies=r.cookies, headers=headers)
    #time.sleep(16)

    ## do checkin
    #url = "http://www.zimuzu.tv/user/sign/dosign"
    #r3 = requests.get(url, cookies=r.cookies, headers=headers)
    #o = r3.json()
    #l.info(r3.content)

def checkin_v2ex(username, password):
    login_url = 'https://v2ex.com/signin'
    home_page = 'https://www.v2ex.com'
    mission_url = 'https://www.v2ex.com/mission/daily'
    headers = {
        'User-Agent' : UA,
        'Host' : "www.v2ex.com",
        'Referer' : 'https://www.v2ex.com/signin',
        'Origin' : 'https://www.v2ex.com'
    }

    v2ex_session = requests.Session()
    # find once
    once_value = search_page(v2ex_session, headers, login_url, 'name', 'once')['value']
    post_info = {
	'u' : username,
	'p' : password,
	'once' : once_value,
	'next' : '/'
    }
    # login
    resp = v2ex_session.post(login_url, data=post_info, headers=headers, verify=True)
    short_url = search_page(v2ex_session, headers, mission_url, 'class', 'super normal button')['onclick']
    first_quote = short_url.find("'")
    last_quote = short_url.find("'", first_quote+1) #str.find(str, beg=0 end=len(string))
    final_url = home_page + short_url[first_quote+1:last_quote]
    l.info(final_url)
    # perform checkin
    page = v2ex_session.get(final_url, headers=headers, verify=True).content
    ok = search_page(v2ex_session, headers, mission_url, 'class', 'fa fa-ok-sign')

def search_page(http, headers, url, tag, name):
    page = http.get(url, headers=headers,verify=True).text
    soup = BeautifulSoup(page, 'lxml')
    soup_result = soup.find(attrs = {tag:name})
    return soup_result

def checkin_smzdm(email, password):
    BASE_URL = 'http://www.smzdm.com'
    LOGIN_URL = BASE_URL + '/user/login/jsonp_check'
    LOGIN_URL = 'https://zhiyou.smzdm.com/user/login/ajax_check'
    CHECKIN_URL = BASE_URL + '/user/qiandao/jsonp_checkin'
    headers = {
        'User-Agent' : UA,
        'Referer': BASE_URL
    }
    params = {
        'user_login': email,
        'user_pass': password,
    }
    l.info(headers)
    l.info(params)
    http = requests.Session()
    r = http.get(BASE_URL, headers=headers)
    r1 = http.get(LOGIN_URL, params=params, headers=headers)
    r2 = http.get(CHECKIN_URL, headers=headers)

checkin_netease(cfg['netease']['music_u'], cfg['netease']['csrf'])
checkin_zimuzu(cfg['zimuzu']['username'], cfg['zimuzu']['password'])
#checkin_v2ex(cfg['v2ex']['username'], cfg['v2ex']['password'])
#checkin_smzdm(cfg['smzdm']['email'], cfg['smzdm']['password'])
