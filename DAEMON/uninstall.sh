#!/bin/bash

TARGET="/etc/init.d/ADdroneDeamon"

if [ "$(id -u)" != "0" ]; then
  echo "This script must be run as root" 2>&1
  exit 1
fi

if [ ! -f $TARGET ]; then
  echo "not installed! ($TARGET)" 2>&1
  exit 1
fi

service ADdroneDeamon stop

sudo update-rc.d ADdroneDeamon remove

rm -rf $TARGET

echo "done"
