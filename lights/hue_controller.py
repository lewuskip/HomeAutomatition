#!/usr/bin/python

from phue import Bridge
import time
import bisect

class HUEServer(object):

    sensorsEvents = {}

    bridgeIP = "192.168.1.103"

    COL_RELAX       = 447
    COL_READ        = 346
    COL_CONCENTRATE = 233
    COL_ENERGIZE    = 156

    BRI_RELAX       = 144
    BRI_READ        = 254
    BRI_CONCENTRATE = 254
    BRI_ENERGIZE    = 254

    lights = {
            "Tymek" : {
                "idx" : 1,
                "status" : {},
                "timeTable" : {
                    0 : { "col" : 1, "value" : 0 },
                    7 : { "col" : 1, "value" : 0 },
                    20 : { "col" : 1, "value" : 0 },
                    21 : { "col" : 1, "value" : 0 },
                    22 : { "col" : 1, "value" : 0 },
                    23 : { "col" : 1, "value" : 0 }
                }
            },

            "Theo"  : {
                "idx" : 2, ""
                "status" : {},
                "timetable" : {
                    0 : { "col" : BRI_RELAX, "value" : 50 },
                    7 : { "col" : BRI_ENERGIZE, "value" : 250 },
                    17 : { "col" : BRI_RELAX, "value" : 255 },
                    20 : { "col" : BRI_READ, "value" : 150 },
                    21 : { "col" : BRI_RELAX, "value" : 100 },
                    22 : { "col" : BRI_RELAX, "value" : 50 },
                    23 : { "col" : BRI_RELAX, "value" : 25 }
                }
            }
    }

    sensorDef = {
            "Tymek" : 2,
            "Theo"  : 5
    }

    BUTTON_ON = 1
    BUTTON_DIM_UP = 2
    BUTTON_DIM_DOWN = 3
    BUTTON_OFF = 4

    def __init__(self):
        self._bridge = Bridge(self.bridgeIP)
        self._bridge.connect()

        for name, idx in self.sensorDef.items():
            self.sensorsEvents[idx] = None

        for name, idx in self.lights.items():
            self.lights[name]["status"] = self._bridge.get_light(self.lights[name]["idx"])

    def getCurrentColor(self, lightDef):
        currHour = int(time.strftime("%H"))

        keys = lightDef["timetable"].keys()
        idx = bisect.bisect_right(keys, currHour) - 1

        selectedDef = lightDef["timetable"][keys[idx]]
        return selectedDef["col"], selectedDef["value"]


    def newEventTheo(self, event):

        # get currentLightSTatus
        self.lights["Theo"]["status"] = self._bridge.get_light(self.lights["Theo"]["idx"])

        ct, bri = self.getCurrentColor(self.lights["Theo"])

        buttonIdx = event / 1000

        if buttonIdx==self.BUTTON_OFF and self.lights["Theo"]["status"]["state"]["on"] == True:
            self._bridge.set_light(self.lights["Theo"]["idx"], "on", False)
        elif buttonIdx==self.BUTTON_ON and self.lights["Theo"]["status"]["state"]["on"] == False:
            print ("setting for Theo", ct, bri)
            self._bridge.set_light(self.lights["Theo"]["idx"], "on", True)
            self._bridge.set_light(self.lights["Theo"]["idx"], "ct", ct)
            self._bridge.set_light(self.lights["Theo"]["idx"], "bri", bri)

            print ( self._bridge.get_light(self.lights["Theo"]["idx"])["state"] )


    def decodeSensorEvents(self, idx, status):
        if self.sensorsEvents[idx] == None:
            self.sensorsEvents[idx] = status["state"]
        else:
            if status["state"]["lastupdated"] != self.sensorsEvents[idx]["lastupdated"]:
                self.sensorsEvents[idx] = status["state"]
                self.newEventTheo( status["state"]["buttonevent"] )


    def start(self):
        while True:
            for name, idx in self.sensorDef.items():
                status = self._bridge.get_sensor(idx)
                self.decodeSensorEvents(idx, status)
            time.sleep(0.1)



if __name__ == "__main__":
    print ("HUE server started")
    hue = HUEServer()
    hue.start()
