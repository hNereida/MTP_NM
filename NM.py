import random
import time

# FUNCIONS I CONSTANTS (ES POSARAN EN UN ALTRE DOCUMENT)

HELLO_RETRIES = 10
TOKEN_RETRIES = 10
DATA_RETRIES = 5
HELLO_TIMEOUT = 1
TOKEN_TIMEOUT = 1
DATA_TIMEOUT = 2

NUM_NODES = 6

HELLO_PACKET = "000"
TOKEN_PACKET = "010"
DATA_PACKET = "100"

my_address = 1
haveData = False
hadToken = False

packet_type = "111"
data = bytearray()

pipes = [0x52, 0x78, 0x41, 0x41, 0x41]

# nodes = { adress: valor, hasData: True or False, hasToken: True or False, toSend: True or False}
nodes = [{"adress": 2, "hasData": False, "hasToken": False, "toSendData": False},
         {"adress": 3, "hasData": False, "hasToken": False, "toSendData": False},
         {"adress": 4, "hasData": False, "hasToken": False, "toSendData": False},
         {"adress": 5, "hasData": False, "hasToken": False, "toSendData": False},
         {"adress": 6, "hasData": False, "hasToken": False, "toSendData": False}]

token = 1

lastNodeNoToken = 0
nodesToSend = []

# VARIABLES

#nodes = FER DICCIONARI QUE SIGUI "NUM_NODE" : (TOKEN, DATA)


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
      	responded, node["hasData"], node["hasToken"] = send_hello(node["adress"]) #TENINT EN COMPTE QUE REPS TRUE OR FALSE NOMÉS SI T'HAN CONTESTAT
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
  	token = read_token()
    if token == 6:
      	return s8()
    return s1()

def s8():
  	print("C'est fini!") # Considerar canvi


  
#Functions to do:  
  
def send_hello(address):
  	responded = False
	self.radio.stopListening()
	self.radio.write(createHelloPacket(address))
	self.radio.startListening()
	if radio.available():
      	# if respons set responded to true
    	pack = radio.read(32)
        dec1=pack>>1
        dec2=pack>>2
    	tok = dec1
    	dat = dec2
	return responded, dat, tok #FER VARIABLE RESPONDED
  
  
def obtain_data_packets():
  	filename = get_file()
	with open(filename,'rb') as f:
        ba = bytearray(f.read())
    os.system("sudo umount -l /mnt/USBDrive")
    to_send = create_list(number_of_files, ba)
 	return to_send
    	

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
def write_file(data):
    with open("/mnt/USBDrive/fileOutput.txt","wb") as f:
        f.write(data)


        
bool is_usb_connected()
bytearray read_usb_file()
int read_token()
send_token(address, token)
send_data(address, data) #includes ACK
wait_hello()