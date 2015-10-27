#!/usr/bin/bash

cd /home/dcai/test_repo/
TT=`date +"%Y-%m-%d"`
date >> log.txt
git commit -a -m "$TT checkin"
#git push origin master -u
