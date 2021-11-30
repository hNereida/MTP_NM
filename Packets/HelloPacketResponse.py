import Packets.PacketsDefinitions as packets
from Packets.PacketsUtils import *
from Packets.PacketGeneric import PacketGeneric

# extends PacketGeneric
class HelloPacketResponse(PacketGeneric):
    # Properties
    hadData = None
    hadToken = None

    # Constructor
    def __init__(self, sourceAddress=0, destAddress=0, hadData=0, hadToken=0):
        # call parent's constructor
        super().__init__(sourceAddress, destAddress, packets.HELLO_RESPONSE["type"])
        self.hadData = hadData
        self.hadToken = hadToken

    # Methods
    # Build packet from local properties
    def buildPacket(self):
        fixedPacket = super().buildPacket()

        # Convert packet to binary string
        packet_string = convertByteArrayToBinaryString(fixedPacket)

        # Add had data field
        length_had_data = getFieldLength(packets.HELLO_RESPONSE["fields"]["had_data"])
        packet_string = addFieldToBinaryString(
            packets.HELLO_RESPONSE["fields"]["had_data"], 
            packet_string,
            getBinaryString(self.hadData, length_had_data)
        )

        # Add had token field
        length_had_token = getFieldLength(packets.HELLO_RESPONSE["fields"]["had_token"])
        packet_string = addFieldToBinaryString(
            packets.HELLO_RESPONSE["fields"]["had_token"], 
            packet_string,
            getBinaryString(self.hadToken, length_had_token)
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
        self.hadData = getNumberFromField(packets.HELLO_RESPONSE["fields"]["had_data"], packet_bitstring)
        # Get had token flag
        self.hadToken = getNumberFromField(packets.HELLO_RESPONSE["fields"]["had_token"], packet_bitstring)

        return True

    # Setters & Getters
    def had_Data(self):
        return self.hadData

    def had_Token(self):
        return self.hadToken