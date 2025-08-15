#!/usr/bin/bash

log=/tmp/gitcheckin.log

DIR=$(dirname "$0")
cd "$DIR" || exit 1
git stash -q
git pull -r -q
TT=$(date +"%Y-%m-%d")
date >>logs/log.txt
if [[ -n "$MONITOR_URL" ]]; then
  curl "$MONITOR_URL?state=run"
fi
git commit -am "$TT checkin" &>"$log"
git push origin master -u &>"$log"
if [[ -n "$MONITOR_URL" ]]; then
  curl "$MONITOR_URL?state=complete"
fi
