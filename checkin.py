#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import requests
import time
import configparser
import os,sys
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client

cfg = configparser.ConfigParser()
dirname=os.path.dirname(os.path.realpath(sys.argv[0]))
cfg.read("{}/credentials.ini".format(dirname))

def checkin_netease(music_u, csrf):
    TYPE_WEBPC = 1
    TYPE_ANDROID = 0
    cookies = {
        'MUSIC_U': music_u,
        '__remember_me': 'true',
        '__csrf': csrf
    }
    headers = {'Referer': 'http://music.163.com/'}
    # web & pc
    url = 'http://music.163.com/api/point/dailyTask?type={}'.format(TYPE_WEBPC)
    response = requests.post(url, cookies=cookies, headers=headers)
    wjson = response.json()
    log_from_code(wjson, 'web & pc')
    # android
    url = 'http://music.163.com/api/point/dailyTask?type={}'.format(TYPE_ANDROID)
    response = requests.post(url, cookies=cookies, headers=headers)
    ajson = response.json()
    log_from_code(ajson, 'android')

def log_from_code(response_json, platform):
    code = response_json['code']
    if code == -2:
        logging.info('{} 失败. 今天签到过了.'.format(platform))
    elif code == 200:
        logging.info('{} ok. 经验 +{}'.format(platform, response_json['point']))
    else:
        logging.info('{} 失败. {}({})'.format(platform, code, response_json['msg']))

def checkin_zimuzu(username, password):
    backurl = 'http://www.zimuzu.tv/user/sign'
    data = {
        'account': username,
        'password': password,
        'remember': 1,
        'url_back': backurl
    }
    headers = {'Referer': 'http://www.zimuzu.tv'}
    r = requests.post("http://www.zimuzu.tv/User/Login/ajaxLogin", data = data, headers=headers)
    o = r.json()
    logging.info(o['info'])

    url = "http://www.zimuzu.tv/user/login/getCurUserTopInfo"
    r1 = requests.get(url, cookies=r.cookies, headers=headers)
    #logging.info(r1.json())

    # open checkin page and wait 16 seconds
    r2 = requests.get(backurl, cookies=r.cookies, headers=headers)
    time.sleep(16)

    # do checkin
    url = "http://www.zimuzu.tv/user/sign/dosign"
    r3 = requests.get(url, cookies=r.cookies, headers=headers)
    o = r3.json()
    logging.info(r3.content)


def _config_log(echo, filename=None):
    #http_client.HTTPConnection.debuglevel = 1
    urllib3_logger = logging.getLogger('urllib3')
    urllib3_logger.setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    if echo:
        if filename:
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(message)s',
                                datefmt='[%Y-%m-%d %H:%M:%S]',
                                filename=filename,
                                filemode='w')
        else:
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(message)s',
                                datefmt='[%Y-%m-%d %H:%M:%S]')

_config_log(True, '/tmp/checkin.log')
checkin_netease(cfg['netease']['music_u'], cfg['netease']['csrf'])
checkin_zimuzu(cfg['zimuzu']['username'], cfg['zimuzu']['password'])
