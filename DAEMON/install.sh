#!/bin/bash

FROM="ADdroneDeamon"
TARGET="/etc/init.d/ADdroneDeamon"

if [ "$(id -u)" != "0" ]; then
  echo "This script must be run as root" 2>&1
  exit 1
fi

if [ -f $TARGET ]; then
  echo "already installed! ($TARGET)" 2>&1
  exit 1
fi

set -e

TMP_FILE="$FROM.tmp"
cp $FROM $TMP_FILE

DIR="$(dirname "`pwd`")"
echo "using dir: $DIR"

sed -i "s@^DIR=.*@DIR='$DIR'@" $TMP_FILE

mv $TMP_FILE $TARGET

echo "checking status...."
service ADdroneDeamon status

echo "enable autostart..."
sudo update-rc.d ADdroneDeamon defaults

echo "installation was successful"
echo ""
echo "\$service ADdroneDeamon {start|stop|restart|status}""

