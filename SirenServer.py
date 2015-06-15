#!/usr/bin/python3

'''
Created on May 25, 2015

@author: Val Blant
'''

import socketserver
from socketserver import TCPServer
import netifaces
import logging
from SirenController import SirenController

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s: %(message)s')
logger = logging.getLogger("SirenServer")

PORT = 8080
IFACE_NAME = 'eth0'
GPIO_PIN = 17

class SirenMessageHandler(socketserver.StreamRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server
    """
    
    def handle(self):
        command = self.rfile.readline().strip().decode("UTF-8")

        logger.info("Received command: %s" % command)
        
        # Dispatch the command
        try:
            if command == "SIREN_ON":
                sirenController.siren_on()
                self.respond("OK\n")
            elif command == "SIREN_OFF":
                sirenController.siren_off()
                self.respond("OK\n")
            else:
                self.respond("FAIL\n")
            
        except Exception as e:
            print(e)
            self.respond("FAIL")
            raise e
    
    def respond(self, message):
        self.wfile.write(bytes(message, 'UTF-8'))



def eth0_ip_address():
    """Discovers the IP address on 'eth0'"""
    
    if ( IFACE_NAME not in netifaces.interfaces() ):
        logger.error(IFACE_NAME, "is not up!")
        raise Exception("Could not find", IFACE_NAME)
    
    eth0_ip = netifaces.ifaddresses(IFACE_NAME)[netifaces.AF_INET][0]['addr']
    
    return eth0_ip
    


# Configure GPIO controller
try:
    sirenController = SirenController(GPIO_PIN)
    sirenController.run_siren_test()
except Exception as e:
    sirenController.cleanup()
    print(e)
    raise e


# Start the network server
eth0_ip = eth0_ip_address()
TCPServer.allow_reuse_address = True
server = TCPServer((eth0_ip, PORT), SirenMessageHandler)

try:
    logger.info("Siren Server listening on %s:%s" % (eth0_ip, PORT))
    server.serve_forever()

except KeyboardInterrupt:
    pass
        
finally:
    server.server_close()
    sirenController.cleanup()
