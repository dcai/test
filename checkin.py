#!/usr/bin/env python3
# -- coding: utf-8 --

import configparser
import logging.config
import os
import socket
import sys
import time
import urllib.request

import requests

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client

# http_client.HTTPConnection.debuglevel = 1

UA = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"

cfg = configparser.ConfigParser(strict=False, interpolation=None)
dirname = os.path.dirname(os.path.realpath(sys.argv[0]))
cfg.read("{}/credentials.ini".format(dirname))

l = logging.getLogger(cfg["logging"]["name"])
l.setLevel(logging.DEBUG)
formatter = logging.Formatter(cfg["logging"]["fmt"])

# create file handler which logs even debug messages
fileHandler = logging.FileHandler(cfg["logging"]["filepath"])
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
l.addHandler(fileHandler)

# create console handler with a higher log level
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.ERROR)
streamHandler.setFormatter(formatter)
l.addHandler(streamHandler)


#  def checkin_netease(music_u, csrf):
#      TYPE_WEBPC = 1
#      TYPE_ANDROID = 0
#      cookies = {"MUSIC_U": music_u, "__remember_me": "true", "__csrf": csrf}
#      headers = {"User-Agent": UA, "Referer": "http://music.163.com/"}
#      # web & pc
#      url = "http://music.163.com/api/point/dailyTask?type={}".format(TYPE_WEBPC)
#      response = requests.post(url, cookies=cookies, headers=headers)
#      wjson = response.json()
#      log_from_code(wjson, "netease: web & pc")
#      # android
#      url = "http://music.163.com/api/point/dailyTask?type={}".format(TYPE_ANDROID)
#      response = requests.post(url, cookies=cookies, headers=headers)
#      ajson = response.json()
#      log_from_code(ajson, "netease: android")
#
#
#  def log_from_code(response_json, platform):
#      code = response_json["code"]
#      if code == -2:
#          l.info("{}: you already checked in today.".format(platform))
#      elif code == 200:
#          l.info("{} OK. +{} points".format(platform, response_json["point"]))
#      else:
#          l.info("{} failed. {}".format(platform, code))
#
#
#  checkin_netease(cfg["netease"]["music_u"], cfg["netease"]["csrf"])


def checkin_smzdm(sess):
    BASE_URL = "http://zhiyou.smzdm.com"
    CHECKIN_URL = BASE_URL + "/user/checkin/jsonp_checkin"
    headers = {"User-Agent": UA, "Referer": BASE_URL}
    http = requests.Session()
    cookies = {"sess": sess}
    r = http.get(CHECKIN_URL, cookies=cookies, headers=headers)
    l.info("{}: {}".format("smzdm", r.json()))


checkin_smzdm(cfg["smzdm"]["sess"])

#  def checkin_zimuzu(domain, username, password):
#      loginUrl = "http://{}/User/Login/ajaxLogin".format(domain)
#      backurl = "http://{}/user/sign".format(domain)
#      data = {
#          "account": username,
#          "password": password,
#          "remember": 0,
#          "url_back": backurl,
#      }
#      headers = {"User-Agent": UA, "Referer": "http://{}".format(domain)}
#      try:
#          r = requests.post(loginUrl, data=data, headers=headers)
#          o = r.json()
#          l.info("{}: [{}] {}".format(domain, username, o["info"]))
#      except Exception as e:
#          l.info("{}: error - {}".format(domain, e))
#
#      # url = "http://www.zimuzu.tv/user/login/getCurUserTopInfo"
#      # r1 = requests.get(url, cookies=r.cookies, headers=headers)
#      ##l.info(r1.json())
#
#      ## open checkin page and wait 16 seconds
#      # r2 = requests.get(backurl, cookies=r.cookies, headers=headers)
#      # time.sleep(16)
#
#      ## do checkin
#      # url = "http://www.zimuzu.tv/user/sign/dosign"
#      # r3 = requests.get(url, cookies=r.cookies, headers=headers)
#      # o = r3.json()
#      # l.info(r3.content)
#
#  zmzdomain="www.rrys2020.com"
#  try:
#      checkin_zimuzu(
#          zmzdomain, cfg["zimuzu"]["username"], cfg["zimuzu"]["password"]
#      )
#      checkin_zimuzu(
#          zmzdomain, cfg["zimuzu2"]["username"], cfg["zimuzu2"]["password"]
#      )
#  except Exception as e:
#      print("checkin_zimuzu error connecting to %s: %s" % (zmzdomain, cfg["zimuzu"]["username"]))


try:
    urllib.request.urlopen(cfg["ping"]["pythoncheckins"], timeout=10)
except socket.error as e:
    l.info("Ping failed: %s" % e)
