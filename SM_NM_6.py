import random
import RF24

# CONSTANTS
import Constants_NM as CNTS

# FUNCIONS AUXILIARS
import Functions_NM as Functions

import Packets.PacketsDefinitions as packets

# VARIABLES
myAddress = 6

haveData = False
hadToken = False

packetType = "111"
fileData = bytearray()
rcvData = bytearray()

# nodes = { address: valor, hasData: True or False, hasToken: True or False, toSend: True or False}
nodes = [{"address": 1, "hasData": False, "hasToken": False, "toSendData": False},
         {"address": 2, "hasData": False, "hasToken": False, "toSendData": False},
         {"address": 3, "hasData": False, "hasToken": False, "toSendData": False},
         {"address": 4, "hasData": False, "hasToken": False, "toSendData": False},
         {"address": 5, "hasData": False, "hasToken": False, "toSendData": False}]

token = 1

lastNodeNoToken = 0
nodesToSendToken = []

# AQUI COMENCEN ELS ESTATS

#Check if we have the USB connected. If we have it connected, we are the first to transmit. If not, we just wait.
def s0():
    global fileData
    Functions.initialize_radio()
    if Functions.is_usb_connected():
    	fileData = Functions.read_usb_file()
    	return s1()
    else: 
        return s4()

#We are the first to transmit -> we have the token. We need to send a hello to everybody reachable.  
def s1():
    global nodes
    global nodesToSendToken
    anyResponded = False
    while not anyResponded:
        for node in nodes:
      	    responded, node["hasData"], node["hasToken"] = Functions.send_hello(myAddress, node["address"])
            if responded:
                anyResponded = True
                nodesToSendToken.append(node["address"])
            if responded and not node["hasData"]:
                node["toSendData"] = True

    return s2()

#Send data
def s2():
    global nodes
    global token
    global lastNodeNoToken
    for node in nodes:
        if node["toSendData"]:
            if Functions.send_data(myAddress, node["address"], fileData): #includes ACK
                node["hasData"] = True
                token += 1
                lastNodeNoToken = node["address"]
            node["toSendData"] = False
    
    return s3()

#Updates token information and sends token to the last device that has received data. 
#If we cannot send the token to the last one (has already had the token or it is unreachable), we need to try to send the token to another.
def s3():
    responded = False
    if lastNodeNoToken > 0:
        responded = Functions.sendToken(myAddress, lastNodeNoToken, token) # (Node address, token)
    while not responded:
        responded = Functions.sendToken(myAddress, random.choice(nodesToSendToken), token)
    return s4()


#State where we wait to reveive a packet
def s4():
    global rcvData
    packet_type, rcvData = Functions.wait_read_packets() #TORNA EL VALOR HELLO_PACKET/DATA_PACKET/TOKEN_PACKET i DATA DEL PAQUET
    if packet_type == packets.HELLO["type"]:
        return s5()
    elif packet_type == packets.DATA["type"]:
      	return s6() # Estat on guardes la data al fitxer
    elif packet_type == packets.TOKEN["type"]:
      	return s7() # Estat on llegeixes el token

def s5():
  	Functions.send_hello_response(myAddress, rcvData, haveData, hadToken)
  	return s4()

# XUCLAR DATA I GUARDAR EN FITXER
def s6():
    global haveData
    Functions.write_file(rcvData) #into raspberry
    haveData = True
    return s4()

#Update the information of the node with the information of the token    
def s7():
    global token
    token = rcvData
    if token == 6:
        return s8()
    return s1()

def s8():
  	print("C'est fini!") # Considerar canvi
    # sys.exit()

def main():
    return s0()

if __name__ == "__main__":
    main()
