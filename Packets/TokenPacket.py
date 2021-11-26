import Packets.PacketsDefinitions as packets
from Packets.PacketsUtils import *
from Packets.PacketGeneric import PacketGeneric

# extends PacketGeneric
class TokenPacket(PacketGeneric):
    # Properties
    num_recv_data = None

    # Constructor
    def __init__(self, sourceAddress=0, destAddress=0, typePacket=0, num_recv_data=0):
        # call parent's constructor
        super().__init__(sourceAddress, destAddress, packets.TOKEN["type"])
        self.num_recv_data = num_recv_data

    # Methods
    # Build packet from local properties
    def buildPacket(self):
        fixedPacket = super().buildPacket()

        # Convert packet to binary string
        packet_string = convertByteArrayToBinaryString(fixedPacket)

        # Add num_recv_data field
        length_num_recv_data = getFieldLength(packets.TOKEN["fields"]["num_recv_data"])
        packet_string = addFieldToBinaryString(
            packets.TOKEN["fields"]["num_recv_data"], 
            packet_string,
            getBinaryString(self.num_recv_data, num_recv_data)
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
        # Get had data flag
        self.num_recv_data = getNumberFromField(packets.TOKEN["fields"]["num_recv_data"], packet_bitstring)

        return True

    # Setters & Getters
    def getNumRecvData(self):
        return self.num_recv_data