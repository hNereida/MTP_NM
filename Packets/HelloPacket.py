# extends PacketGeneric
class HelloPacket(PacketGeneric):
    # Constructor
    def __init__(self, sourceAddress, destAddress, typePacket):
        # call parent's constructor
        super().__init__(sourceAddress, destAddress, typePacket)
    
    # no variable packet part, so no custom build and parse functions

    