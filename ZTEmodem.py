import urllib2
import json


#
#this is a simple read-only interacate for usb ZTE modem
#
class ZTEmodem:

  #subscribe to this values
  cmds=[
    'modem_main_state',
    'network_provider',
    'network_type',
    'rssi',
    'wan_ipaddr','ipv6_wan_ipaddr',
    'realtime_tx_bytes','realtime_rx_bytes']

  #note: lte related:
  # lte_band, lte_rsrp, lte_rsrq, lte_pci, lte_rssi

  commandsUrl="http://192.168.0.1/goform/goform_get_cmd_process?"


  def getModemData(self):

    url=ZTEmodem.commandsUrl
    url+="&isTest=false"
    url+="&cmd="+('%2C'.join(ZTEmodem.cmds))
    url+="&multi_data=1"

    try:
      req = urllib2.Request(url)
      req.add_header('Referer','http://192.168.0.1/index.html')
      resp = urllib2.urlopen(req)

      html=resp.read()
      return json.loads(html)
    except:
      return None



if __name__ == "__main__":
  modem = ZTEmodem()
  data=modem.getModemData()
  if data:
    print json.dumps(data,indent=2)
  else:
    print "error"
