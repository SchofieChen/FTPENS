import time
import RPi.GPIO as GPIO
import logging
from logging.config import fileConfig
from logging.handlers import TimedRotatingFileHandler
import datetime
from ftplib import FTP


log_filename = datetime.datetime.now().strftime("./Log/%Y-%m-%d_%H_%M.log")
fileConfig('./Log/logging_config.ini', defaults={"log_filename":log_filename})
logger = logging.getLogger()

BUTTON_PIN = 18
LED_PIN = 23


## FTP file information
filename = 'CUSOVTLeakEvent_SubGrp_20200728.txt'
bufsize = 1024


ftp = FTP('F12AENS')
ftp.login(user='ens_ftp', passwd = 'ftpens')
ftp.cwd('ENS_FILE/dat')

def GPIO_detect_callback(channel):
    logging.info('Pressed the Button')
    with open(filename,'rb') as f:
        ftp.storbinary('STOR '+filename, f)
        ftp.quit()
	#detected massage
	
	#Action after detected


    #GPIO.output(LED_PIN, GPIO.HIGH)
	#time.sleep(0.1)
	#GPIO.output(LED_PIN, GPIO.LOW)
    



GPIO.setmode(GPIO.BCM)


GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=GPIO_detect_callback, bouncetime=250)

try:
	logging.info('Press Ctrl-C to Stop')
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	logging.info('Shutdown Program')
finally:
	GPIO.cleanup()
