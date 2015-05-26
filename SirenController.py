'''
Created on May 25, 2015

@author: Val Blant
'''

import RPi.GPIO as GPIO
from flufl.enum import Enum
import time
import logging

class SirenState(Enum):
    ON = GPIO.HIGH
    OFF = GPIO.LOW

class SirenController:
    
    def __init__(self, control_pin):
        self.logger = logging.getLogger("SirenController")
        self._control_pin = control_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(control_pin, GPIO.OUT, initial=GPIO.LOW)
        self.logger.info("Siren Controller initialized on pin %s." % control_pin)
        
        self.siren_off()
        
    def run_siren_test(self):
        self.logger.info("Initiating self-test...")
        self.siren_on()
        time.sleep(3)
        self.siren_off()
        self.logger.info("Self-test completed.")
    
    def siren_on(self):
        self._status = SirenState.ON
        self._update_control_pin()

    def siren_off(self):
        self._status = SirenState.OFF
        self._update_control_pin()
    
    def cleanup(self):
        self.logger.info("Cleaning up GPIO pins...")

        GPIO.cleanup()
        
    def _update_control_pin(self):
        GPIO.output(self._control_pin, int(self._status))
        self._print_status()
        
    def _print_status(self):
        self.logger.info("Siren is " + self._status.name)
