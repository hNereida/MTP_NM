import Packets.PacketsDefinitions as packets
from Packets.PacketsUtils import *
from Packets.PacketGeneric import PacketGeneric

# extends PacketGeneric
class DataPacket(PacketGeneric):
    # Properties
    length = None # int
    eot = None # int
    sequence_number = None # int
    payload = None # bytes

    # Constructor
    def __init__(self, sourceAddress=0, destAddress=0, typePacket=0, length=0, eot=0, sequence_number=0, payload=[]):
        # call parent's constructor
        super().__init__(sourceAddress, destAddress, packets.DATA["type"])
        self.length = length
        self.eot = eot
        self.sequence_number = sequence_number
        self.payload = payload

    # Methods
    # Build packet from local properties
    def buildPacket(self):
        fixedPacket = super().buildPacket()

        # Convert packet to binary string
        packet_string = convertByteArrayToBinaryString(fixedPacket)

        # Add length field
        length_length = getFieldLength(packets.DATA["fields"]["length"])
        packet_string = addFieldToBinaryString(
            packets.DATA["fields"]["length"], 
            packet_string,
            getBinaryString(self.length, length_length)
        )

        # Add eot field
        length_eot = getFieldLength(packets.DATA["fields"]["eot"])
        packet_string = addFieldToBinaryString(
            packets.DATA["fields"]["eot"], 
            packet_string,
            getBinaryString(self.eot, length_eot)
        )
        
        # Add sequence number field
        length_seq_number = getFieldLength(packets.DATA["fields"]["sequence_number"])
        packet_string = addFieldToBinaryString(
            packets.DATA["fields"]["sequence_number"], 
            packet_string,
            getBinaryString(self.sequence_number, length_seq_number)
        )

        # Add payload
        packet_string = addFieldToBinaryString(
            packets.DATA["fields"]["payload"], 
            packet_string,
            convertByteArrayToBinaryString(self.payload)
        )
        
        # Convert string binary to ByteArray
        createdPacket = convertBinaryStringToByteArray(packet_string)
        return createdPacket


    # Parse packet from received bytearray and stores info in
    # local properties
    def parsePacket(self, packet_bytes):
        super().parsePacket(packet_bytes)

        # Assume that the packet has been correctly identified by type
        # Convert packet to binary string
        packet_bitstring = convertByteArrayToBinaryString(packet_bytes)

        self.length = getNumberFromField(packets.DATA["fields"]["length"], packet_bitstring)
        self.eot = getNumberFromField(packets.DATA["fields"]["eot"], packet_bitstring)
        self.sequence_number = getNumberFromField(packets.DATA["fields"]["sequence_number"], packet_bitstring)
        
        field_binary = stripBinaryStringFromPacket(packet.DATA["fields"]["payload"], packet_bitstring, self.length*8)
        self.payload = convertBinaryStringToByteArray(field_binary)

        return True

    # Setters & Getters
    def isEoT(self):
        return self.eot

    def getSequenceNumber(self):
        return self.sequence_number

    def getPayload(self):
        return self.payload