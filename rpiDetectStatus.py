#!/usr/bin/env python
import RPi.GPIO as GPIO
import re,time

#setup initial program requirements
checkFile = "/opt/some/place/to/find/data.txt"
timeDelaySec = 5
switchControlPin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(switchControlPin, GPIO.OUT)
# 11 pin is 6 pins down from the 3.3v on upper left, one down from ground, max source output == 16 mA 
searchPattern = re.compile(r'^you.+(?P<numMessages>[0-9]+).+')

# search pattern parses out from text file:
# you recieved 1 new message

def checkForMessages():
    numMessages = 0
    with open(checkFile,'r') as fileIn:
        lines = fileIn.readlines()
        for line in lines:
            match = searchPattern.search(str(line))
            if match:
                numMessages = int(match.group('numMessages'))
                return numMessages
            else:
                pass
    print("[STDERR]: regex failed, exiting program now")
    GPIO.cleanup()
    exit(1)

if __name__ == '__main__':
    while True:
        try:
            numberOfMessages = checkForMessages()
            if numberOfMessages > 0:
                GPIO.output(switchControlPin,GPIO.HIGH)
            else:
                GPIO.output(switchControlPin,GPIO.LOW)
            time.sleep(timeDelaySec)
        except:
            break
    print("[STDERR]: error detected, program exiting now")
    GPIO.cleanup()
    exit(1)