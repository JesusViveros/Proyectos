#!/usr/bin/env python
from naoqi import ALProxy

def main(robotIp,robotPort):
    sensorProxy = ALProxy("ALSensors",robotIp,robotPort)
    memoryProxy = ALProxy("ALMemory",robotIp,robotPort)

    sensorProxy.subscribe("myApplication")
    memory.subscribeToEvent("Evento","RightBumperPressed","RightBumperPressed")

    rbp=memory.getData("RightBumperPressed")
    print rbp
    # Please read Sonar ALMemory keys section if you want to know the other values you can get.
    memory.unsubscribeToEvent("Evento","RightBumperPressed")
    sensorProxy.unsubscribe("myApplication")

if __name__ == "__main__":
    robotIp = "148.226.225.94"
    robotPort = 9559
    main(robotIp,robotPort)