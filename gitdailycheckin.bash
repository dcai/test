#!/bin/bash

cd ~/test/
git stash -q
git pull -r -q
TT=$(date +"%Y-%m-%d")
date >>log.txt
git commit -a -m "$TT checkin" &>/dev/null
git push origin master -u &>/dev/null
