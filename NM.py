import random
import time
import os
import RF24

# CONSTANTS (ES POSARAN EN UN ALTRE DOCUMENT)

HELLO_RETRIES = 10
TOKEN_RETRIES = 10
DATA_RETRIES = 5
HELLO_TIMEOUT = 1
TOKEN_TIMEOUT = 1
DATA_TIMEOUT = 2

NUM_NODES = 6

HELLO_PACKET = "000"
HELLO_RESPONSE = "001"
TOKEN_PACKET = "010"
DATA_PACKET = "100"
DATA_ACK_PACKET = "011"
TOKEN_ACK_PACKET = "101"

pipes = [0x52, 0x78, 0x41, 0x41, 0x41]

# VARIABLES
my_address = 1

haveData = False
hadToken = False

packet_type = "111"
data = bytearray()

# nodes = { adress: valor, hasData: True or False, hasToken: True or False, toSend: True or False}
nodes = [{"adress": 2, "hasData": False, "hasToken": False, "toSendData": False},
         {"adress": 3, "hasData": False, "hasToken": False, "toSendData": False},
         {"adress": 4, "hasData": False, "hasToken": False, "toSendData": False},
         {"adress": 5, "hasData": False, "hasToken": False, "toSendData": False},
         {"adress": 6, "hasData": False, "hasToken": False, "toSendData": False}]

token = 1

lastNodeNoToken = 0
nodesToSend = []

# IMPORTAR FUNCIONS DEFINIDES PER GRUP B --> ADAPTAR FUNCIONS FETES AMB LES SEVES FUNCIONS

# FUNCIONS AUXILIARS (ES POSARAN EN UN ALTRE DOCUMENT)

def is_usb_connected():
    usbpath = "/media/pi/" # Modificar per cada raspberry
    isconnected = False
    time.sleep(5)
    if len(os.listdir(os.path.dirname(usbpath))) != 0:
        usb = os.listdir(os.path.dirname(usbpath))[0]
        time.sleep(5)
        files = os.listdir(os.path.join(usbpath, usb))
        if len(files) != 0:
            isconnected = True
    return isconnected

def read_usb_file():
    usbpath = "/media/pi/" # Modificar per cada raspberry
    usb = os.listdir(os.path.dirname(usbpath))[0]
    files = os.listdir(os.path.join(usbpath, usb))
    filename = files[0]
    file = open(os.path.join(usbpath, usb, filename), "rb")
    data = file.read()
    file.close()
    return data

# Fer import de radio, mirar el self
# MIRAR COM S'ADAPTA AMB LES FUNCIONS DEL TEAM B
# UTILITZAR LES CONSTANTS DE RETRIES I TIMEOUTS
def send_hello(dest_address):
  	responded = False
    hasData = False
    hadToken = False
    radio = RF24.RF24()
	radio.stopListening()
    # Part Team B
    hello_packet = PacketName(my_adress, dest_address, HELLO_PACKET)
    packetToSend = PacketName.buildPacket()
	radio.write(packetToSend)
    # Part Team B
    # Esperar un temps???
	radio.startListening()
	if radio.available(): # buscar funcio per mirar si hi ha dades rebudes IMPORTANT!!! (potser es aquesta)
        # IMPLEMENTAR TIMEOUTS I RETRIES???
        responded = True
    	rcvBytes = radio.read(32)
        rcvPacket = packetName()
        rcvPacket.parsePacket(rcvBytes)
        if rcvPacket.getField3() == HELLO_RESPONSE: # No se si es modificarar el nom getField3()
            hasData = rcvPacket.getField4() # No se si es modificarar el nom getField4()
            hadToken = rcvPacket.getField5() # No se si es modificarar el nom getField5()
    return responded, hasData, hadToken

# Retorna true si la data s'ha enviat correctament
# Falta implementar la funcio
def send_data(address, data):
    return True
  
# ACABAR FUNCIO
# MIRAR COM S'ADAPTA MAB LES FUNCIONS DEL TEAM B
def obtain_data_packets():
  	filename = get_file()
	with open(filename,'rb') as f:
        ba = bytearray(f.read())
    os.system("sudo umount -l /mnt/USBDrive")
    to_send = create_list(number_of_files, ba)
 	return to_send

# FER LA FUNCIO
def create_list(number_of_files, bytearray):
    return to_send

# Fer import de radio
# Declarar EOT
# MIRAR COM S'ADAPTA MAB LES FUNCIONS DEL TEAM B
# ACABAR FUNCIO
def send_data(address):
    radio.openWritingPipe(pipesbytes)
    radio.powerUp()
    pack=0
    identifier = "010" #identifier Data packet
    for temp in to_send:
        for x in range(0,len(temp),31):
            data = identifier + pack
            aux = bytearray(data.to_bytes(1,'big')) + temp[x:x+31]
            while not(radio.write(aux)):    
                print("failed delivery ")
        pack+=1
    while not(radio.write(EOT)):    
        print("failed delivery " )
        time.sleep(0.01)

# Fer import de radio
# Declarar EOT
# MIRAR COM S'ADAPTA MAB LES FUNCIONS DEL TEAM B
# ACABAR FUNCIO
def wait_read_packets():
	radio.openReadingPipe(1, pipesbytes)
    radio.startListening()
    while EOT not in receivedPacket:
        if radio.available():
            receivedPacket = radio.read(32)
            cabacera = receivedPacket[0]
            logic = bool(data2 & 0x01)
            dec = data2>>1
            if EOT not in receivedPacket:
                if seq == logic:
                    received[dec]=received[dec] + receivedPacket[1:32] 
                    seq=not seq     
    for dataReceived in received:
        finalData.extend(dataReceived)
    return finalData

# CANVIAR A GUARDAR A RASPBERRY
# ACABAR LA FUNCIO
def write_file(data):
    with open("/mnt/USBDrive/fileOutput.txt","wb") as f:
        f.write(data)

# AQUI COMENCEN ELS ESTATS

#Check if we have the USB connected. If we have it connected, we are the first to transmit. If not, we just wait.
def s0():
	if is_usb_connected():
    	data = read_usb_file()
    	return s1()
	else: 
		return s4()

#We are the first to transmit -> we have the token. We need to send a hello to everybody reachable.  

def s1():
	for node in nodes:
      	responded, node["hasData"], node["hasToken"] = send_hello(node["adress"])
        if responded and not node["hasData"]:
			node["toSendData"] = True
	return s2()

#Send data
def s2():
	for node in nodes:
		if node["toSendData"]:
			if send_data(node["adress"], data): #includes ACK
            	node["hasData"] = True
                token += 1
                lastNodeNoToken = node["adress"]
	return s3()

#Updates token information and sends token to the last device that has received data. 
#If we cannot send the token to the last one (has already had the token or it is unreachable), we need to try to send the token to another.
def s3():
  	for node in nodes:
      	if node["toSendData"]:
      		nodesToSend.append(node["adress"])
	if lastNodeNoToken > 0:
		sendToken(lastNodeNoToken, token) # (Node adress, token)
    else:
      	sendToken(random.choice(nodesToSend), token)
    return s4()


#State where we wait to reveive a packet
def s4():
	packet_type, data = wait_read_packets() #TORNA EL VALOR HELLO_PACKET/DATA_PACKET/TOKEN_PACKET i DATA DEL PAQUET
    if packet_type == HELLO_PACKET:
    	return s5()
    else if packet_type == DATA_PACKET:
      	return s6() # MODIFICAR PER ESTAT ON ESPERES EL TOKEN
    else if packet_type == TOKEN_PACKET:
      	return s7() # Estel que at on esperes la data

def s5():
	send_hello_response(haveData, hadToken) # Definir funció
	if not haveData:
    return s5()

def s6():
  	# XUCLAR DATA I GUARDAR EN FITXER
    write_file(data) #into raspberry
    haveData = True
    return s4()

#Update the information of the node with the information of the token    
def s7():
    send_token_ack() # no se is cal aixo
  	token = read_token()
    if token == 6:
      	return s8()
    return s1()

def s8():
  	print("C'est fini!") # Considerar canvi



# #Functions to do:
# int read_token()
# send_token(address, token)
# send_data(address, data) #includes ACK
# send_token_ack() # no se si cal aquesta funcio