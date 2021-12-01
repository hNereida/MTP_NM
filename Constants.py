import RF24

# GROUP DEPENDENT
# Hardware
CE = 25 # RPi Chip Enable pin
ADDRESS = 3 # Each device's address



# GROUP INDEPENDENT
# Constants
RETRIES = 5 # Check documentation
TIMEOUT = 0.001 # (s) Check documentation
SENDER = True
RECEIVER = False


# Declare EOT

# NRF24 constants
DATARATE = RF24.RF24_1MBPS
POWERLEVEL = RF24.RF24_PA_HIGH
CHANNEL = 6
ENCODING_TRANSMISSION = 'utf-8'
PACKET_SIZE = 32
DATA_SIZE = 30
pipes_aux = [0x52, 0x78, 0x41, 0x41, 0x41]
PIPES = bytearray(pipes_aux)
