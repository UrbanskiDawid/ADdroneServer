#!/bin/bash
#
# this is a script to autostart ADdroneServer.py
# and some tools in seperate terminals (GUI windows)
#
set -e

brandName="ADdrone"

title="THIS IS $brandName log view window"
xterm -geometry 115x65 -hold -T "$brandName: logs" -e "echo $title;echo 'wait 10sec...'; sleep 10s; l=\`ls -1t logs/ | head -n1\`; echo \"using '\$l'\"; tail -f logs/\$l;" &

title="THIS IS $brandName trace log window";
portNum=5555
xterm -geometry 115x65 -hold -T "$brandName: TCPdump" -e "echo $title;sudo bash tools/tcpDump.sh $portNum" &

echo "starting server..."
python ADdroneServer.py

