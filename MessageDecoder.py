class MessageDecoder:
  def tryToReadMessage(self, msg):
    try:
      data=b64decode( msg )
    except:
      return False
    i=-1;
    if len(data)>=31 and data[0]==36 and data[1]==36 and data[2]==36:
      print('received ADdrone message ')
      print("prefix",data[0],data[0],data[2])
      #axis
      axis1=struct.unpack('f', bytes([data[ 6],data[ 5],data[ 4],data[ 3]]))[0]
      axis2=struct.unpack('f', bytes([data[10],data[ 9],data[ 8],data[ 7]]))[0]
      axis3=struct.unpack('f', bytes([data[14],data[13],data[12],data[11]]))[0]
      #not in use
      zero1=struct.unpack('f', bytes([data[18],data[17],data[16],data[15]]))[0]
      zero2=struct.unpack('f', bytes([data[22],data[21],data[20],data[19]]))[0]
      zero3=struct.unpack('f', bytes([data[26],data[25],data[24],data[23]]))[0]
      #
      CRC=struct.unpack('f', bytes([data[30],data[29],data[28],data[27]]))[0]
      nl=struct.unpack('c',bytes( [data[31]] ))[0]
      print("axis1=",axis1," axis2:",axis2," axis3:",axis3,"CRC",CRC," lastChar:",nl)
      return True
    return False