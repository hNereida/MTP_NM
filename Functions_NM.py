import random
import time
import os
import RF24

# CONSTANTS 
import Constants_NM as CNTS
import Packets.PacketsDefinitions as packets

# IMPORTAR FUNCIONS DEFINIDES PER GRUP B --> ADAPTAR FUNCIONS FETES AMB LES SEVES FUNCIONS
from Packets.HelloPacket import HelloPacket
from Packets.HelloPacketResponse import HelloPacketResponse
from Packets.DataPacket import DataPacket
from Packets.DataPacketResponse import DataPacketResponse
from Packets.TokenPacket import TokenPacket
from Packets.TokenPacketResponse import TokenPacketResponse

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
def send_hello(source_address, dest_address):
    responded = False
    hasData = False
    hadToken = False
    radio = RF24.RF24()
    radio.stopListening()
    # Part Team B
    hello_packet = HelloPacket(source_address, dest_address)
    packetToSend = hello_packet.buildPacket()
    radio.write(packetToSend)
    # Part Team B
    # Esperar un temps??? --> GP: not sure
    time.sleep(0.1)

     # buscar funcio per mirar si hi ha dades rebudes IMPORTANT!!! (potser es aquesta)
    radio.startListening()
    while not radio.available():
      time.sleep(CNTS.TIMEOUT)

    # IMPLEMENTAR TIMEOUTS I RETRIES???
    responded = True
    rcvBytes = radio.read(radio.payloadSize)
    rcvPacket = HelloPacketResponse()
    rcvPacket.parsePacket(rcvBytes)
    if rcvPacket.getTypePacket() == packets.HELLO_RESPONSE["type"]:
        hasData = rcvPacket.hadData() 
        hadToken = rcvPacket.hadToken()
    return responded, hasData, hadToken

# Declarar EOT
# Retorna true si la data s'ha enviat correctament
# MIRAR COM S'ADAPTA MAB LES FUNCIONS DEL TEAM B
# ACABAR FUNCIO
def send_data(myAddress, toAddress, data):
    radio = RF24.RF24()
    radio.begin(25,0) #set CE and IRQ pins
    radio.setDataRate(CNTS.DATARATE) 
    radio.setChannel(CNTS.CHANNEL) #Set Channel 6
    radio.setRetries(1,CNTS.RETRIES) #250us*i , 4 retries - es pot canviar
    radio.setPALevel(CNTS.POWERLEVEL) #0 dBm power amplifier level - see table in docu https://nrf24.github.io/RF24/classRF24.html
    radio.openWritingPipe(bytearray(CNTS.PIPES))
    radio.powerUp()
    pack=0
    #FUNCIO GRUP B createDataPacket(myAddress,toAddress,data)
    identifier = CNTS.DATA_PACKET #identifier Data packet
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
        return False
    return True

def send_token(sourceAddress, toAddress, numRecvData):
    radio = RF24.RF24()
    radio.begin(25,0) #set CE and IRQ pins
    radio.setDataRate(RF24.RF24_1MBPS) 
    radio.setChannel(0x4c) #Set Channel 76
    radio.setRetries(1,4) #250us*i , 4 retries - es pot canviar
    radio.setPALevel(RF24.RF24_PA_MAX) #0 dBm power amplifier level - see table in docu https://nrf24.github.io/RF24/classRF24.html
    radio.openWritingPipe(bytearray(CNTS.PIPES))
    radio.powerUp()
    pack=0

    #FUNCIO GRUP B createTokenPacket(toAddress,token)
    tokenPacket = TokenPacket(sourceAddress, toAddress, numRecvData)
    token = tokenPacket.buildPacket()

    while not(radio.write(token)):    
      print("failed delivery ")
      #return False

    return True

# Fer import de radio
# Declarar EOT
# MIRAR COM S'ADAPTA MAB LES FUNCIONS DEL TEAM B
# ACABAR FUNCIO
def wait_read_packets():
    finalData = ""
    radio.openReadingPipe(1, pipesbytes)
    radio.startListening()

    
    # Group B
    # Read one packet
    while not radio.available():
        time.sleep(0.01)
    receivedPacket = radio.read(32)

    if PacketGeneric.isPacket(receivedPacket, packets.HELLO["type"]):
        helloPacket = HelloPacket()
        helloPacket.parsePacket(receivedPacket)
        # do whatever with the packet

    elif PacketGeneric.isPacket(receivedPacket, packets.HELLO_RESPONSE["type"]):
        helloResponsePacket = HelloResponsePacket()
        helloResponsePacket.parsePacket(receivedPacket)
        # do whatever with the packet

    # TODO: Check sequence number for Stop & Wait
    elif PacketGeneric.isPacket(receivedPacket, packets.DATA["type"]):
        dataPacket = DataPacket()
        dataPacket.parsePacket(receivedPacket)
        finalData = dataPacket.getPayload()

    while not dataPacket.isEot():
        while not radio.available():
            time.sleep(0.01)
        receivedPacket = radio.read(32)
        dataPacket.parsePacket(receivedPacket)
        finalData.extend(dataPacket.getPayload())

    # TODO: Check sequence number for Stop & Wait
    elif PacketGeneric.isPacket(receivedPacket, packets.DATA_RESPONSE["type"]):
        dataResponsePacket = DataResponsePacket()
        dataResponsePacket.parsePacket(receivedPacket)
        # do whatever with the packet

    elif PacketGeneric.isPacket(receivedPacket, packets.TOKEN["type"]):
        tokenPacket = TokenPacket()
        tokenPacket.parsePacket(receivedPacket)
        # do whatever with the packet

    elif PacketGeneric.isPacket(receivedPacket, packets.TOKEN_RESPONSE["type"]):
        tokenResponsePacket = TokenResponsePacket()
        tokenResponsePacket.parsePacket(receivedPacket)
    # do whatever with the packet

    """
    while EOT not in receivedPacket:
        while not radio.available():
          time.sleep(0.01)

        receivedPacket = radio.read(32)
        header = receivedPacket[0]
        #Multiplico la header per 00001110 per quedarme amb els bits on hi ha la info del packet
        if (header&0x0E) == 0x00:
            return finalData, CNTS.HELLO_PACKET
        elif (header&0x0E) == 0x02:
            return finalData, CNTS.HELLO_RESPONSE
        elif (header&0x0E) == 0x04: 
            seqReceived = bool(header & 0x01)
            dec = header>>1
            if EOT not in receivedPacket:
                if seq == seqReceived:
                    received[dec]=received[dec] + receivedPacket[1:32] 
                    seq=not seq    
        elif (header&0x0E) == 0x06:
            return finalData, CNTS.DATA_ACK
        elif (header&0x0E) == 0x08:
            return finalData, CNTS.TOKEN_PACKET
        elif (header&0x0E) == 0x0A:
            return finalData, CNTS.TOKEN_ACK 
    for dataReceived in received:
        finalData.extend(dataReceived)
    return finalData, CNTS.DATA_PACKET
"""
# CANVIAR A GUARDAR A RASPBERRY
# ACABAR LA FUNCIO
def write_file(data):
    with open("/mnt/USBDrive/fileOutput.txt","wb") as f:
        f.write(data)

# #Functions to do:
# int read_token()
# send_token(address, token)
# send_token_ack() # no se si cal aquesta funcio
