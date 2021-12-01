import RF24

# CONSTANTS

RETRIES = 4 # Mirar si s'ha de modificar
TIMEOUT = 0.1 # (en segons) Mirar si s'ha de modificar
SENDER = True
RECEIVER = False

# DECLARAR EOT

# DECLARAR LES CONSTANTS DEL MODUL NRF24
DATARATE = RF24.RF24_1MBPS
POWERLEVEL = RF24.RF24_PA_MAX
CHANNEL = 6
ENCODING_TRANSMISSION = 'utf-8'
PACKET_SIZE = 32
DATA_SIZE = 30
pipes_aux = [0x52, 0x78, 0x41, 0x41, 0x41]
PIPES = bytearray(pipes_aux)
