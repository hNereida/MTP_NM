import Packets.PacketsDefinitions as packets
from Packets.PacketsUtils import *
from Packets.PacketGeneric import PacketGeneric

# extends PacketGeneric
class DataPacketResponse(PacketGeneric):
    # Properties
    sequence_number = None
    ack_nack = None

    # Constructor
    def __init__(self, sourceAddress=0, destAddress=0, typePacket=0, sequence_number=0, ack_nack=0):
        # call parent's constructor
        super().__init__(sourceAddress, destAddress, packets.DATA_RESPONSE["type"])
        self.sequence_number = sequence_number
        self.ack_nack = ack_nack

    # Methods
    # Build packet from local properties
    def buildPacket(self):
        fixedPacket = super().buildPacket()

        # Convert packet to binary string
        packet_string = convertByteArrayToBinaryString(fixedPacket)

        # Add sequence_number field
        length_sequence_number = getFieldLength(packets.DATA_RESPONSE["fields"]["sequence_number"])
        packet_string = addFieldToBinaryString(
            packets.DATA_RESPONSE["fields"]["sequence_number"], 
            packet_string,
            getBinaryString(self.sequence_number, length_sequence_number)
        )

        # Add ack_nack field
        length_ack_nack = getFieldLength(packets.DATA_RESPONSE["fields"]["ack_nack"])
        packet_string = addFieldToBinaryString(
            packets.DATA_RESPONSE["fields"]["ack_nack"], 
            packet_string,
            getBinaryString(self.length_ack_nack, length_ack_nack)
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
        # Get sequence number
        self.sequence_number = getNumberFromField(packets.DATA_RESPONSE["fields"]["sequence_number"], packet_bitstring)
        # Get ack-nack
        self.ack_nack = getNumberFromField(packets.DATA_RESPONSE["fields"]["ack_nack"], packet_bitstring)

        return True

    # Setters & Getters
    def isValid(self):
        return self.ack_nack

    def getSequenceNumber(self):
        return self.sequence_number