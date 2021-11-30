import Constants_NM as constants

# Add binary string field to string of binary
def addFieldToBinaryString(field_parameters, str, field):
    bit_start = field_parameters["byte_start"]*8 + field_parameters["bit_start"]  
    bit_end = bit_start + len(field) - 1
    str = str[:bit_start] + field + str[bit_end+1:]
    return str

# Get field length
def getFieldLength(field_parameters):
    bit_start = field_parameters["byte_start"]*8 + field_parameters["bit_start"]

    if(field_parameters["static"]):
        bit_end = field_parameters["byte_end"]*8 + field_parameters["bit_end"]
    else:
        bit_end = 8*constants.PACKET_SIZE - 1

    return (bit_end + 1 - bit_start)

# Get Binary string from field
def getBinaryString(data, lengthBits=0):
    # return format(data, "0"+ str(lengthBits) +"b")
    return bin(data)[2:].zfill(lengthBits)

# Convert binary string to bytes
def convertBinaryStringToByteArray(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')


# Convert ByteArray to bitstring
def convertByteArrayToBinaryString(packet_bytes):
    result = ""
    for i in range(0, len(packet_bytes)):
        result = result + format(packet_bytes[i], "08b")
    return result

def stripBinaryStringFromPacket(field_parameters, packet_bitstring, length=0):
    start_bit = field_parameters["byte_start"]*8 + field_parameters["bit_start"]
    if field_parameters["static"]:
        end_bit = field_parameters["byte_end"]*8+  field_parameters["bit_end"]
    else:
        end_bit = start_bit + length - 1
    return packet_bitstring[start_bit:(end_bit+1)] 

# Convert bytes to string
def getStringFromField(field_parameters, packet_bitstring, length=0):
    field_binary = stripBinaryStringFromPacket(field_parameters, packet_bitstring, length)
    field_byte_array = convertBinaryStringToByteArray(field_binary)
    return field_byte_array.decode(constants.ENCODING_TRANSMISSION)

# Get field number to int
def getNumberFromField(field_parameters, packet_bitstring):
    field_binary = stripBinaryStringFromPacket(field_parameters, packet_bitstring)
    return int(field_binary, 2)





