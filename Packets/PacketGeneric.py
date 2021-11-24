class PacketGeneric():
    # Properties
    sourceAddress = None # int
    destAddress = None # int
    typePacket = None # int
    
    # Constructor
    def __init__(self, sourceAddress, destAddress, typePacket):
        self.sourceAddress = sourceAddress
        self.destAddress = destAddress
        self.typePacket = typePacket

    # Methods
    # Build packet from local properties
    def buildPacket(self):

    # Parse packet from received bytearray and stores info in
    # local properties
    def parsePacket(self, packet_bytes):

    # Check if it is a packet of this type
    def isPacket(self,packet_bytes, typePacket):

    # Setters & Getters
    def getSourceAddress(self):
        return self.sourceAddress

    def getDestinationAddress(self):
        return self.destinationAddress

    def getTypePacket(self):
        return self.typePacket

    
