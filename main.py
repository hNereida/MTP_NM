import sys
import random
import RF24

# Constants
import Constants as CNTS

# Auxiliary functions
import Functions

# Packets
import Packets.PacketsDefinitions as packets

# Init variables
addresses = []
myAddress = 0

nodes = []

haveData = False
hadToken = False

packetType = "111"
fileData = bytearray()
rcvData = bytearray()


def generate_nodes(myAddress):
    global addresses
    global nodes
    for i in range(1, 7):
        if i != myAddress:
            addresses.append(i)
    
    nodes = [{"address": addresses[0], "hasData": False, "hasToken": False, "toSendData": False},
         {"address": addresses[1], "hasData": False, "hasToken": False, "toSendData": False},
         {"address": addresses[2], "hasData": False, "hasToken": False, "toSendData": False},
         {"address": addresses[3], "hasData": False, "hasToken": False, "toSendData": False},
         {"address": addresses[4], "hasData": False, "hasToken": False, "toSendData": False}]

token = 1
lastNodeNoToken = 0
nodesToSendToken = []

# AQUI COMENCEN ELS ESTATS

#Check if we have the USB connected. If we have it connected, we are the first to transmit. If not, we just wait.
def s0():
    print("S0")
    global fileData
    Functions.initialize_radio()
    if Functions.is_usb_connected():
        print("s0 -> s1, USB connected")
        fileData = Functions.read_usb_file()
        return s1()
    else:
        print("s0 -> s4, USB not connected")
        return s4()

#We are the first to transmit -> we have the token. We need to send a hello to everybody reachable.
def s1():
    print("S1")
    global nodes
    global nodesToSendToken
    anyResponded = False
    while not anyResponded:
        for node in nodes:
            print("s1: Sending a HELLO packet to " + str(node["address"]))
            responded, node["hasData"], node["hasToken"] = Functions.send_hello(myAddress, node["address"])
            print("Responded Fora: " + str(responded))
            if responded:
                anyResponded = True
                nodesToSendToken.append(node["address"])
            if responded and not node["hasData"]:
                node["toSendData"] = True

    print("s1 -> s2")
    return s2()

#Send data
def s2():
    print("S2")
    global nodes
    global token
    global lastNodeNoToken
    for node in nodes:
        if node["toSendData"]:
            print("Node que enviare data: " + str(node))
            if Functions.send_data(myAddress, node["address"], fileData): #includes ACK
                node["hasData"] = True
                token += 1
                lastNodeNoToken = node["address"]
            node["toSendData"] = False

    print("s2 -> s3")
    return s3()

#Updates token information and sends token to the last device that has received data.
#If we cannot send the token to the last one (has already had the token or it is unreachable), we need to try to send the token to another.
def s3():
    print("S3")
    responded = False
    if lastNodeNoToken > 0:
        responded = Functions.send_token(myAddress, lastNodeNoToken, token) # (Node address, token)
    while not responded:
        responded = Functions.send_token(myAddress, random.choice(nodesToSendToken), token)

    print("s3 -> s4")
    return s4()


#State where we wait to reveive a packet
def s4():
    print("S4")
    global rcvData
    packet_type, rcvData = Functions.wait_read_packets(myAddress) #TORNA EL VALOR HELLO_PACKET/DATA_PACKET/TOKEN_PACKET i DATA DEL PAQUET
    if packet_type == packets.HELLO["type"]:
        print("s4 -> s5")
        return s5()
    elif packet_type == packets.DATA["type"]:
        print("s4 -> s6")
        print("rcvData: " + str(rcvData))
        return s6() # Estat on guardes la data al fitxer
    elif packet_type == packets.TOKEN["type"]:
        print("s4 -> s7")
        return s7() # Estat on llegeixes el token

def s5():
    print("S5")
    Functions.send_hello_response(myAddress, rcvData, haveData, hadToken)
    print("s5: Sending a HELLO_RESPONSE packet to " + str(rcvData))
    print("s5: Have data " + str(haveData))
    print("s5: Have token " + str(hadToken))
    print("s5 -> s4")
    return s4()

# XUCLAR DATA I GUARDAR EN FITXER
def s6():
    print("S6")
    global haveData
    Functions.write_file(rcvData) #into raspberry
    haveData = True
    print("s6 -> s4")
    return s4()

#Update the information of the node with the information of the token
def s7():
    print("S7")
    global token
    token = rcvData
    if token == 6:
        print("s7 -> s8")
        return s8()
    print("s7 -> s1")
    return s1()

def s8():
    print("S8")
    print("s8: DONE!") # Considerar canvi
    # sys.exit()

def main():
    return s0()

if __name__ == "__main__":
    myAddress = int(sys.argv[1])
    print("my address = " + str(myAddress))
    generate_nodes(myAddress)
    print("nodes = " + str(nodes))
    main()
