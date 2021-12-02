import Packets.PacketsDefinitions as packets
from Packets.PacketsUtils import *
from Packets.PacketGeneric import PacketGeneric

# extends PacketGeneric
class HelloPacket(PacketGeneric):
    # Constructor
    def __init__(self, sourceAddress=0, destAddress=0):
        # call parent's constructor
        super().__init__(sourceAddress, destAddress, packets.HELLO["type"])
    
    # no variable packet part, so no custom build and parse functions

    