import time
import os
import math
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
from Packets.PacketGeneric import PacketGeneric

# Variables

radio = None

# FUNCIONS AUXILIARS (ES POSARAN EN UN ALTRE DOCUMENT)

def initialize_radio(): # quan es para la radio?
    global radio
    radio = RF24.RF24()
    radio.begin(25,0)
    radio.setDataRate(CNTS.DATARATE)
    radio.setChannel(CNTS.CHANNEL) 
    radio.setRetries(1, CNTS.RETRIES)
    radio.setPALevel(CNTS.POWERLEVEL)
    radio.openWritingPipe(CNTS.PIPES)
    radio.openReadingPipe(1, CNTS.PIPES)
    radio.powerUp()
    return radio


def is_usb_connected():
    usbpath = "/media/pi/" # Modificar per cada raspberry
    isconnected = False
    time.sleep(0.01)
    if len(os.listdir(os.path.dirname(usbpath))) != 0:
        usb = os.listdir(os.path.dirname(usbpath))[0]
        time.sleep(0.01)
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
def send_hello(srcAddress, rcvAddress):
    responded = False
    hasData = False
    hadToken = False
    helloPacket = HelloPacket(srcAddress, rcvAddress)
    packetToSend = helloPacket.buildPacket()
    
    retries = 0
    while retries < CNTS.RETRIES and not responded:
        radio.stopListening()
        radio.write(packetToSend)
        radio.startListening()
        time.sleep(CNTS.TIMEOUT)
        if radio.available():
            responded = True
        retries += 1
    
    rcvBytes = radio.read(CNTS.PACKET_SIZE)
    rcvPacket = HelloPacketResponse()
    rcvPacket.parsePacket(rcvBytes)
    if rcvPacket.getTypePacket() == packets.HELLO_RESPONSE["type"]:
        hasData = rcvPacket.hadData() 
        hadToken = rcvPacket.hadToken()
    return responded, hasData, hadToken


def send_hello_response(srcAddress, rcvAddress, haveData, hadToken):
    helloPacketResponse = HelloPacketResponse(srcAddress, rcvAddress, haveData, hadToken)
    packetToSend = helloPacketResponse.buildPacket()
    radio.stopListening()
    radio.write(packetToSend)


# Declarar EOT
# Retorna true si la data s'ha enviat correctament
# MIRAR COM S'ADAPTA MAB LES FUNCIONS DEL TEAM B
# ACABAR FUNCIO
def send_data(srcAddress, rcvAddress, fileData):
    sentPackets = 0
    EOF = False
    sequenceNumber = False
    packetSize = CNTS.DATA_SIZE
    for x in range(0, len(fileData), 30):
        sentPackets += 1
        if sentPackets == math.ceil(len(fileData)/30):
            packetSize = len(fileData) - (sentPackets-1)*30
            EOF = True
        dataPacket = DataPacket(srcAddress, rcvAddress, packetSize, EOF, sequenceNumber, fileData[x:x+packetSize])

        responded = False
        retries = 0
        while retries <= CNTS.RETRIES and not responded:
            radio.stopListening()
            radio.write(dataPacket)
            radio.startListening()
            time.sleep(CNTS.TIMEOUT)
            if radio.available():
                rcvBytes = radio.read(CNTS.PACKET_SIZE)
                rcvPacket = DataPacketResponse()
                rcvPacket.parsePacket(rcvBytes)
                # Check if it is the right packet type
                if sequenceNumber == rcvPacket.getSequenceNumber() and rcvPacket.isValid():
                    responded = True
                else:
                    retries += 1
            else:
                retries += 1
            
        sequenceNumber = not sequenceNumber

        if retries > CNTS.RETRIES and not responded:
            return False
    
    return True

def send_token(srcAddress, rcvAddress, token):
    responded = False
    tokenPacket = TokenPacket(srcAddress, rcvAddress, token)
    packetToSend = tokenPacket.buildPacket()
    
    retries = 0
    while retries < CNTS.RETRIES and not responded:
        radio.stopListening()
        radio.write(packetToSend)
        radio.startListening()
        time.sleep(CNTS.TIMEOUT)
        if radio.available():
            rcvBytes = radio.read(CNTS.PACKET_SIZE)
            rcvPacket = TokenPacketResponse()
            rcvPacket.parsePacket(rcvBytes)
            # Check if it is the right packet type
            if rcvPacket.isValid():
                responded = True
            else:
                retries += 1
        else:
            retries += 1    

    return responded

# Fer import de radio
# Declarar EOT
# MIRAR COM S'ADAPTA MAB LES FUNCIONS DEL TEAM B
# ACABAR FUNCIO
def wait_read_packets():
    finalData = ""
    radio.startListening()

    # Group B
    # Read one packet
    while not radio.available():
        time.sleep(0.01)
    rcvBytes = radio.read(CNTS.PACKET_SIZE)

    if PacketGeneric.isPacket(rcvBytes, packets.HELLO["type"]):
        helloPacket = HelloPacket()
        helloPacket.parsePacket(rcvBytes)
        return packets.HELLO["type"], helloPacket.getSourceAddress()

    # TODO: Check sequence number for Stop & Wait
    if PacketGeneric.isPacket(rcvBytes, packets.DATA["type"]):
        dataPacket = DataPacket()
        dataPacket.parsePacket(rcvBytes)
        finalData = dataPacket.getPayload()

        # SORTIR DEL WHILE QUANT NO ES DATA
        sequenceNumber = False
        while not dataPacket.isEot():
            while not radio.available():
                time.sleep(0.01)
            receivedPacket = radio.read(CNTS.PACKET_SIZE)
            dataPacket.parsePacket(receivedPacket)
            # Check CRC
            if dataPacket.getSequenceNumber == sequenceNumber:
                dataPacketResponse = DataPacketResponse(dataPacket.getDestinationAddress, dataPacket.getSourceAddress, sequenceNumber, True)
            else:
                dataPacketResponse = DataPacketResponse(dataPacket.getDestinationAddress, dataPacket.getSourceAddress, sequenceNumber, False)
            packetToSend = dataPacketResponse.buildPacket()
            radio.stopListening()
            radio.write(packetToSend)
            radio.startListening()

            finalData.extend(dataPacket.getPayload())

        return packets.DATA["type"], finalData

    if PacketGeneric.isPacket(rcvBytes, packets.TOKEN["type"]):
        tokenPacket = TokenPacket()
        tokenPacket.parsePacket(rcvBytes)
        # We should check with the CRC that the packet is okey, value True of below
        tokenPacketResponse = TokenPacketResponse(tokenPacket.getDestinationAddress, tokenPacket.getSourceAddress, True)
        packetToSend = tokenPacketResponse.buildPacket()
        radio.stopListening()
        radio.write(packetToSend)

        return packets.TOKEN["type"], tokenPacket.getNumRecvData()


# CANVIAR A GUARDAR A RASPBERRY
# ACABAR LA FUNCIO
def write_file(data):
    with open("/mnt/USBDrive/fileOutput.txt","wb") as f:
        f.write(data)
