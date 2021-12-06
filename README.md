# MTP_NM
MTP Network Mode repository

## To modify by each group
- Constants.py -- Change the address here
- ioparent.py -- Change the switches and leds here

## Program structure
- top_level.py -- Reads USB, waits for the GO signal to execute main.py, kills it after 300 seconds
-	main.py -- The program that contains the state machine, can only run for 5 minutes
