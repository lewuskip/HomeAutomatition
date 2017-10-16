#!/usr/bin/python

from phue import Bridge
import time


class HUEServer(object):

    sensorsEvents = {}

    bridgeIP = "192.168.1.103"

    lightsDef = {
            "Tymek" : 1,
            "Theo"  : 2
    }

    sensorDef = {
            "Tymek" : 2
    }

    def __init__(self):
        self._bridge = Bridge(self.bridgeIP)
        self._bridge.connect()

        for name, idx in self.sensorDef.items():
            self.sensorsEvents[idx] = None

    def lightEvent(self):


        pass

    def decodeSensorEvents(self, idx, status):
        if self.sensorsEvents[idx] == None:
            self.sensorsEvents[idx] = status["state"]
        else:
            if status["state"]["lastupdated"] != self.sensorsEvents[idx]["lastupdated"]:
                self.sensorsEvents[idx] = status["state"]
                print (status["state"])


    def start(self):
        while True:

            for name, idx in self.sensorDef.items():
                status = self._bridge.get_sensor(idx)
                self.decodeSensorEvents(idx, status)
            time.sleep(0.2)
            #print ( selfs._bridge.get_light(1) )



if __name__ == "__main__":
    print ("HUE server started")
    hue = HUEServer()
    hue.start()
