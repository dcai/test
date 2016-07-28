#!/usr/bin/bash

cd /home/dcai/test/
git stash -q
git pull -r
TT=`date +"%Y-%m-%d"`
date >> log.txt
git commit -a -m "$TT checkin" &> /dev/null
git push origin master -u &> /dev/null
