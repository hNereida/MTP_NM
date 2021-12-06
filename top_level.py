import ioparent
from time import sleep
import os
import time

# Constants
import Constants as CNTS
# Functions
import Functions


def main():

    has_started = False
    haveData = False
    ioparent.config()
    os.system("sudo rm -r " + CNTS.working_directory) # Clean, so that if it exists it means the USB has been read
    while True:

        try:

            # Read USB and store its file if connected
            if not haveData and not has_started:
                if Functions.is_usb_connected():
                    print("USB connected")
                    Functions.copy_usb_file()
                    haveData = True


            SW = ioparent.read_switches() # get switches config, decide which son to run, add logic below
            SW_GO = SW[ioparent.MASTER_SWITCH]

            if (SW_GO and not has_started):
                has_started = True
                time_start = time.time()
                os.system("python3 " + CNTS.main_file + " " + str(CNTS.ADDRESS) + " &") # Start main
            if (has_started):
                if (time.time() - time_start > 300): # kill
                    os.system("bash " + CNTS.kill_file)

            sleep(0.1) 
        except Exception as e:
            print(e)
            os.system("bash " + CNTS.kill_file)
            exit()



if __name__ == "__main__":
    main()
