import RF24

# GROUP DEPENDENT
# Hardware
CE = 25 # RPi Chip Enable pin

# Paths
working_directory = '/home/pi/working-directory/'
is_usb_connected = '/home/pi/MTP_NM/bash/usb_id.sh'
read_usb = '/home/pi/MTP_NM/bash/read_usb.sh'
output_file = 'NM_received.txt'

timeout_file = '/home/pi/MTP_NM/timeout.py'
main_file = '/home/pi/MTP_NM/main.py'
kill_file = '/home/pi/MTP_NM/kill.sh'

ADDRESS = 3




# GROUP INDEPENDENT
# Constants
RETRIES = 5 # Check documentation
# TIMEOUT = 0.001 # (s) Check documentation
# TIMEOUT = 0.01 # (s) Check documentation
TIMEOUT = 0.3 # (s) Check documentation

NM_DURATION = 300 # 5 minutes expressed in secs

SENDER = True
RECEIVER = False


# NRF24 constants
DATARATE = RF24.RF24_1MBPS
# POWERLEVEL = RF24.RF24_PA_HIGH
POWERLEVEL = RF24.RF24_PA_LOW
CHANNEL = 6
ENCODING_TRANSMISSION = 'utf-8'
PACKET_SIZE = 32
DATA_SIZE = 30
PIPES_VECTOR = [0x52, 0x78, 0x41, 0x41, 0x41]
PIPES = bytearray(PIPES_VECTOR)
