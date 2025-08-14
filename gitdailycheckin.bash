#!/usr/bin/bash

DIR=$(dirname "$0")
cd "$DIR" || exit 1
git stash -q
git pull -r -q
TT=$(date +"%Y-%m-%d")
date >>logs/log.txt
git commit -am "$TT checkin" &>/dev/null
git push origin master -u &>/dev/null
