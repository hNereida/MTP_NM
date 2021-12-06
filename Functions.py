import time
import os
import RF24
import subprocess

# CONSTANTS
import Constants as CNTS
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
    command = "bash " + CNTS.is_usb_connected
     
    # Call command
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
     
    # Get terminal output
    (output, err) = p.communicate()
     
    # Wait for wait and determine
    p_status = p.wait()

    if ("dev" in str(output)):
        print("USB stick connected")
        return(True)
    else:
        print("USB stick not connected")
        return(False)

    
def get_file():
    #USB detection check, TODO: LED indication

    subprocess.call(['sh', CNTS.read_usb]) #AFEGIT PER NOSALTRES (TEAM C)

    txt_files = [f for f in os.listdir(CNTS.working_directory) if f.endswith('.txt')]
    filename = txt_files[0]
    return CNTS.working_directory+filename

def read_usb_file():
    filename = get_file()
    with open(filename,'rb') as f:
        ba = bytearray(f.read())
    return ba

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
    while retries <= CNTS.RETRIES and not responded:
        radio.stopListening()
        radio.write(packetToSend)
        radio.startListening()
        time.sleep(CNTS.TIMEOUT)
        print("HELLO retries: " + str(retries) + " to node " + str(rcvAddress))
        if radio.available():
            rcvBytes = radio.read(CNTS.PACKET_SIZE)
            rcvPacket = HelloPacketResponse()
            rcvPacket.parsePacket(rcvBytes)
            if rcvPacket.getTypePacket() == packets.HELLO_RESPONSE["type"] and rcvPacket.getDestinationAddress() == srcAddress:
                responded = True
                print("received")
                hasData = rcvPacket.had_Data()
                hadToken = rcvPacket.had_Token()
            else:
                retries += 1
        else:
            retries += 1
    return responded, hasData, hadToken


def send_hello_response(srcAddress, rcvAddress, haveData, hadToken):
    helloPacketResponse = HelloPacketResponse(srcAddress, rcvAddress, haveData, hadToken)
    packetToSend = helloPacketResponse.buildPacket()
    radio.stopListening()
    radio.write(packetToSend)

# ---------------------------------------------------------
def getNumberPackets(str_bytes):
    num_packets = int(len(str_bytes)/CNTS.DATA_SIZE)
    if not len(str_bytes)%CNTS.DATA_SIZE == 0:
      num_packets = num_packets + 1
    
    return num_packets
 
def createDataPackets(str_bytes):
    # Get number packets to send
    num_packets = getNumberPackets(str_bytes)
    # Get length of the last packet
    last_packet_length = len(str_bytes) - (int(len(str_bytes)/CNTS.DATA_SIZE)*CNTS.DATA_SIZE)
 
    # Array of data packets
    dataPackets = []
 
    # Sequence number is going to be filled with 0,1 as for stop & wait protocol
    x = 0
    while x < num_packets:
      if x == num_packets-1:
        dataPackets.append(str_bytes[x*CNTS.DATA_SIZE:])
      else:
        dataPackets.append(str_bytes[x*CNTS.DATA_SIZE:CNTS.DATA_SIZE*(x+1)])
      x = x + 1
    
    return dataPackets

# ---------------------------------------------------------

# Declarar EOT
# Retorna true si la data s'ha enviat correctament
# MIRAR COM S'ADAPTA MAB LES FUNCIONS DEL TEAM B
# ACABAR FUNCIO
def send_data(srcAddress, rcvAddress, fileData):
    sentPackets = 0
    EOF = False
    sequenceNumber = False

    packets = createDataPackets(fileData)
    print("Packets: " + str(packets))

    for x in range(0, len(packets)):
        sentPackets += 1

        if x == len(packets)-1:
            EOF = True
            
        dataPacket = DataPacket(srcAddress, rcvAddress, len(packets[x]), EOF, sequenceNumber, packets[x])
        print("Payload DataPacket: " + str(packets[x]) + "Sequence number: " + str(sequenceNumber))
        packetToSend = dataPacket.buildPacket()
        responded = False
        retries = 0
        while retries < CNTS.RETRIES and not responded:
            radio.stopListening()
            radio.write(packetToSend)
            radio.startListening()
            time.sleep(CNTS.TIMEOUT)
            if radio.available():
                rcvBytes = radio.read(CNTS.PACKET_SIZE)
                rcvPacket = DataPacketResponse()
                rcvPacket.parsePacket(rcvBytes)
                print("ACK Data Sequence Number: " + str(rcvPacket.getSequenceNumber()))
                # Check if it is the right packet type
                if sequenceNumber == rcvPacket.getSequenceNumber() and rcvPacket.isValid() and rcvPacket.getDestinationAddress() == srcAddress:
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
        print("TOKEN SENT, TOKEN VALUE: " + str(token))
        radio.startListening()
        time.sleep(CNTS.TIMEOUT)
        if radio.available():
            rcvBytes = radio.read(CNTS.PACKET_SIZE)
            rcvPacket = TokenPacketResponse()
            rcvPacket.parsePacket(rcvBytes)
            # Check if it is the right packet type
            if rcvPacket.isValid() and rcvPacket.getDestinationAddress() == srcAddress:
                responded = True
                print("THE RECEIVER HAS THE TOKEN")
            else:
                retries += 1
        else:
            retries += 1

    return responded

# Fer import de radio
# Declarar EOT
# MIRAR COM S'ADAPTA MAB LES FUNCIONS DEL TEAM B
# ACABAR FUNCIO
def wait_read_packets(myAddress):
    finalData = ""
    radio.startListening()
    received = False
    # Group B
    # Read one packet

    while not received:
        while not radio.available():
            time.sleep(0.01)
        rcvBytes = radio.read(CNTS.PACKET_SIZE)
        packetGeneric = PacketGeneric()
        packetGeneric.parsePacket(rcvBytes)

        if packetGeneric.getDestinationAddress() == myAddress:

            if packetGeneric.isPacket(rcvBytes, packets.HELLO["type"]):
                helloPacket = HelloPacket()
                helloPacket.parsePacket(rcvBytes)
                return packets.HELLO["type"], helloPacket.getSourceAddress()

            # TODO: Check sequence number for Stop & Wait
            if packetGeneric.isPacket(rcvBytes, packets.DATA["type"]):
                dataPacket = DataPacket()
                dataPacket.parsePacket(rcvBytes)
                finalData = dataPacket.getPayload()

                # SORTIR DEL WHILE QUAN NO ES DATA
                sequenceNumber = False
                while not dataPacket.isEoT():
                    while not radio.available():
                        time.sleep(0.01)
                    receivedPacket = radio.read(CNTS.PACKET_SIZE)
                    dataPacket.parsePacket(receivedPacket)
                    # Check CRC
                    if dataPacket.getSequenceNumber() == sequenceNumber and dataPacket.getDestinationAddress() == myAddress:
                        dataPacketResponse = DataPacketResponse(dataPacket.getDestinationAddress(), dataPacket.getSourceAddress(), sequenceNumber, True)
                        sequenceNumber = not sequenceNumber
                    else:
                        dataPacketResponse = DataPacketResponse(dataPacket.getDestinationAddress(), dataPacket.getSourceAddress(), sequenceNumber, False)
                    packetToSend = dataPacketResponse.buildPacket()
                    radio.stopListening()
                    radio.write(packetToSend)
                    radio.startListening()
                    # sequenceNumber = not sequenceNumber

                    finalData += dataPacket.getPayload()
                    print("Payload Data: " + str(dataPacket.getPayload()))
                print("Final Data: " + str(finalData))
                return packets.DATA["type"], finalData

            if packetGeneric.isPacket(rcvBytes, packets.TOKEN["type"]):
                print("HE REBUT EL TOKEN")
                tokenPacket = TokenPacket()
                tokenPacket.parsePacket(rcvBytes)
                # We should check with the CRC that the packet is okey, value True of below
                tokenPacketResponse = TokenPacketResponse(tokenPacket.getDestinationAddress(), tokenPacket.getSourceAddress(), True)
                packetToSend = tokenPacketResponse.buildPacket()
                radio.stopListening()
                radio.write(packetToSend)
                print("HE ENVIAT EL TOKEN RESPONSE")
                return packets.TOKEN["type"], tokenPacket.getNumRecvData()

            received = True
    print("Si no entra a cap if del wait_read_packet el tipus es: " + str(packetGeneric.getTypePacket()))
    return packetGeneric.getTypePacket(), bytearray()


# CANVIAR A GUARDAR A RASPBERRY
# ACABAR LA FUNCIO
def write_file(data):
    if not os.path.exists(CNTS.working_directory):
        os.system("mkdir " + CNTS.working_directory)
    with open(CNTS.working_directory + CNTS.output_file, "w+b") as f:
        f.write(data)
