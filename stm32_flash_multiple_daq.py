
# STM32 Falsher with DAQ 6001 _2022-08 SEPT

################################################
# install Ni-DAQmx 14.0
# install Python 3.7.2 or higher 32bit
# install st-link uitility v4.5
#pip install nidaqmx
#pip install pyserial
#pip install colorama
################################################

import nidaqmx
import subprocess
import sys
import time
import serial
from colorama import Fore ,Back , Style
import datetime

import os

# Specify the file path to store the counter value
file_path ="C:/x.text"

# Check if the file exists, and if not, create it with an initial value of 0
if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        f.write("0")

# Read the current counter value from the file
with open(file_path, "r") as f:
    counter = int(f.read())


    
# Initialize DAQ Device for PB_In
task_pb = nidaqmx.Task()
task_pb.di_channels.add_di_chan("Dev1/port0/line0")
task_pb.start()

# Initialize DAQ Device for Relay_Out
task_rel = nidaqmx.Task()
task_rel.do_channels.add_do_chan("Dev1/port0/line1")
task_rel.start()

# Disable USB/STM Flashers for User to avoid any Short Circuit at Loading PCB Panel step
##########################################
task_rel.write(False)
##########################################
# notify user to press start button
print ("")
print ("Product Name: “xx“")
print("***Press Pb to Start***")

#stm32 flasher serial number
id1 = "SN=13005400150000385134534E"
id2 = "SN=51FF6E064882575137381587"
id3 = "SN=3C42110011145157544D4E00"
id4 = "SN=153D0C0011145157544D4E00"
id5 = "SN=38480F0011145157544D4E00"


def flashing(idn):
    res = subprocess.run(["C:\Program Files (x86)\STMicroelectronics\STM32 ST-LINK Utility\ST-LINK Utility\ST-LINK_CLI.exe", "-c",idn, "SWD", "-P",
                          'C:/x.hex',"-OB","RDP=1","BOR_LEV=0","IWDG_SW=1","nRST_STOP=1","nRST_STDBY=1","-V","-rOB","-Rst"], shell=True )
    _status = res.returncode
    if _status > 0 :
       print()
       print(Fore.RED + Style.BRIGHT   +   'Flashing...... [ERROR]   ')
       print()
    # check if return Just (0) not all status !
    if _status == 0 :
       print()
       print(Fore.GREEN + Style.BRIGHT +   'Flashing...... [OK]   ')
       print()
    return _status
       

def flash_result(idx , idx_status):
        _idx = idx
        _idx_status = idx_status
        print (Fore.RED +'['+ str(_idx)+ ']' "ERR") if _idx_status > 0 else print (Fore.GREEN +'['+ str(_idx)+ ']' "OK")



while True:
    
    time.sleep(0.1)
    pb_state=task_pb.read()
    
    if pb_state==True:
 ##########################################       
        # Enable USB port
        task_rel.write(True)
 ##########################################
        # USB initial set up time
        print (" USB Port Init...    ")
        time.sleep(2)
        print (" USB Port Init... [Done]   ")
        print (" GUI VER [1.1]   ")
        print (" ...   ")
        time.sleep(3)
        print (" ")
        print (" ")
        # Increment the counter value
        counter += 1

        # Write the updated counter value back to the file
        with open(file_path, "w") as f:
            f.write(str(counter))

        if counter >= 10000:
            exit()
##########################################
        id1_status = flashing(id1)
        id2_status = flashing(id2)
        id3_status = flashing(id3)
        id4_status = flashing(id4)
        id5_status = flashing(id5)
        time.sleep(0.2)
 ##########################################       
        # Terminate usb Port    
        #task_rel.write(True)
 ##########################################
        e = datetime.datetime.now()
        print (Fore.WHITE +'*'*13 +'Flash Report' +'*'*10)
        print (Fore.WHITE +' '*11 +"Date : %s-%s-%s"%(e.day,e.month,e.year))
       # print (Fore.WHITE +' Product Name : xxxx')
       # print (Fore.WHITE +'Flash Report :')
        print (Fore.WHITE +'*'*35)
        
        '''
        res_num = [1,2,3,4,5]
        for i in res_num:
            flash_result(i , id1_status)
        '''    
        flash_result(1 , id1_status)
        flash_result(2 , id2_status)
        flash_result(3 , id3_status)
        flash_result(4 , id4_status)
        flash_result(5 , id5_status)
        print (Fore.WHITE +'*'*35)

       
       
        print(Fore.RED + Style.BRIGHT   +   '***Press Pb to Start***')
        print (Fore.WHITE +'')
       # print("[[Press Pb to Start]]")
        
        time.sleep(0.2)
        task_rel.write(False)
       
    if pb_state == False:
         pass

