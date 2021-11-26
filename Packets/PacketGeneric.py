import Packets.PacketsDefinitions as packets
from Packets.PacketsUtils import *
from Packets.PacketGeneric import PacketGeneric

class PacketGeneric():
    # Properties
    sourceAddress = None # int
    destAddress = None # int
    typePacket = None # int
    
    # Constructor
    def __init__(self, sourceAddress=0, destAddress=0, typePacket=0):
        self.sourceAddress = sourceAddress
        self.destAddress = destAddress
        self.typePacket = typePacket

    # Methods
    # Build packet from local properties
    def buildPacket(self):
         # Create empty packet
        packet_string = format(0, "0" + str(32*8) + "b")

        # Add source address
        length_source_address = getFieldLength(packets.FIXED_PART["fields"]["source_address"])
        packet_string = addFieldToBinaryString(
            packets.FIXED_PART["fields"]["source_address"], 
            packet_string,
            getBinaryString(self.sourceAddress, length_source_address)
        )

        # Add destionation address
        length_dest_address = getFieldLength(packets.FIXED_PART["fields"]["destination_address"])
        packet_string = addFieldToBinaryString(
            packets.FIXED_PART["fields"]["destination_address"], 
            packet_string,
            getBinaryString(self.destAddress, length_dest_address)
        )

        # Add type
        length_type = getFieldLength(packets.FIXED_PART["fields"]["type"])
        packet_string = addFieldToBinaryString(
            packets.FIXED_PART["fields"]["type"], 
            packet_string,
            getBinaryString(self.typePacket, length_type)
        )

         # Convert string binary to ByteArray
        createdPacket = convertBinaryStringToByteArray(packet_string)
        return createdPacket


    # Parse packet from received bytearray and stores info in
    # local properties
    def parsePacket(self, packet_bytes):
        # Assume that the packet has been correctly identified by type
        # Convert packet to binary string
        packet_bitstring = convertByteArrayToBinaryString(packet_bytes)
        # Get Source Address
        self.sourceAddress = getNumberFromField(packets.FIXED_PART["fields"]["source_address"], packet_bitstring)
        # Get Destination Address
        self.destAddress = getNumberFromField(packets.FIXED_PART["fields"]["destination_address"], packet_bitstring)

        return True

    # Check if it is a packet of this type
    @staticmethod
    # Check if it is a packet of this type
    def isPacket(self, packet_bytes, typePacket): # Convert packet to binary string
        packet_bitstring = convertByteArrayToBinaryString(packet_bytes)
        type_packet = getNumberFromField(packets.FIXED_PART["fields"]["type"], packet_bitstring)
        return type_packet == typePacket

    # Setters & Getters
    def getSourceAddress(self):
        return self.sourceAddress

    def getDestinationAddress(self):
        return self.destinationAddress

    def getTypePacket(self):
        return self.typePacket
