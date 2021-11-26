import random
import time
import os
import RF24

# CONSTANTS
import Constants_NM as CNTS

# FUNCIONS AUXILIARS
import Functions_NM as Functions

# VARIABLES
myAddress = 1

haveData = False
hadToken = False

packetType = "111"
fileData = bytearray()
rxData = bytearray()

# nodes = { adress: valor, hasData: True or False, hasToken: True or False, toSend: True or False}
nodes = [{"adress": 2, "hasData": False, "hasToken": False, "toSendData": False},
         {"adress": 3, "hasData": False, "hasToken": False, "toSendData": False},
         {"adress": 4, "hasData": False, "hasToken": False, "toSendData": False},
         {"adress": 5, "hasData": False, "hasToken": False, "toSendData": False},
         {"adress": 6, "hasData": False, "hasToken": False, "toSendData": False}]

token = 1

lastNodeNoToken = 0
nodesToSend = []

# AQUI COMENCEN ELS ESTATS

#Check if we have the USB connected. If we have it connected, we are the first to transmit. If not, we just wait.
def s0():
    global fileData
    if Functions.is_usb_connected():
    	fileData = Functions.read_usb_file()
    	return s1()
    else: 
        return s4()

#We are the first to transmit -> we have the token. We need to send a hello to everybody reachable.  
def s1():
    global nodes
    for node in nodes:
      	responded, node["hasData"], node["hasToken"] = Functions.send_hello(myAddress, node["adress"])
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
            if Functions.send_data(myAddress, node["adress"], fileData): #includes ACK
                node["hasData"] = True
                token += 1
                lastNodeNoToken = node["adress"]
    return s3()

#Updates token information and sends token to the last device that has received data. 
#If we cannot send the token to the last one (has already had the token or it is unreachable), we need to try to send the token to another.
def s3():
    global nodesToSend
    for node in nodes:
        if node["toSendData"]:
            nodesToSend.append(node["adress"])
    if lastNodeNoToken > 0:
        Functions.sendToken(lastNodeNoToken, token) # (Node adress, token)
    else:
        Functions.sendToken(random.choice(nodesToSend), token)
    return s4()


#State where we wait to reveive a packet
def s4():
    global rxData
    packet_type, rxData = Functions.wait_read_packets() #TORNA EL VALOR HELLO_PACKET/DATA_PACKET/TOKEN_PACKET i DATA DEL PAQUET
    if packet_type == CNTS.HELLO_PACKET:
        return s5()
    elif packet_type == CNTS.DATA_PACKET:
      	return s6() # Estat on guardes la data al fitxer
    elif packet_type == CNTS.TOKEN_PACKET:
      	return s7() # Estat on llegeixes el token

def s5():
  	Functions.send_hello_response(myAddress, haveData, hadToken)
  	if not haveData:
  	  	return s5()

# XUCLAR DATA I GUARDAR EN FITXER
def s6():
    global haveData
    Functions.write_file(rxData) #into raspberry
    haveData = True
    return s4()

#Update the information of the node with the information of the token    
def s7():
    global token
    token = Functions.read_token()
    if token == 6:
        return s8()
    return s1()

def s8():
  	print("C'est fini!") # Considerar canvi
    # sys.exit()
