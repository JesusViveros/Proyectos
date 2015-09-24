#!/usr/bin/env python
from naoqi import ALProxy 
import rospy
from nao.msg import naomss

def talker(val):
    pub = rospy.Publisher('Sonar',naomss,queue_size=4)
    rospy.init_node('Sensors', anonymous=True)
    rate = rospy.Rate(10)
    pub.publish(val)
    rate.sleep()

def main(robotIp,robotPort):
    sonarProxy = ALProxy("ALSonar",robotIp,robotPort)
    sonarProxy.subscribe("Sensores")
    memoryProxy = ALProxy("ALMemory",robotIp,robotPort)
    while (1):
        # Get sonar left first echo (distance in meters to the first obstacle).
        left=memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        right=memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        val=[left,right]
        print val
        talker(val)

    sonarProxy.unsubscribe("Sensores")

if __name__ == "__main__":
    robotIp = "148.226.225.94"
    robotPort = 9559
    main(robotIp,robotPort)
