#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from naoqi import ALProxy

def talker(val):
    pub = rospy.Publisher('TactilTouch',String,queue_size=4)
    rospy.init_node('Sensor', anonymous=True)
    rate = rospy.Rate(10)
    pub.publish(val)
    rate.sleep()

def main(robotIp,robotPort):
    sensor = ALProxy("ALSensors",robotIp,robotPort)
    memory = ALProxy("ALMemory",robotIp,robotPort)

    sensor.subscribe("myApplication")
    memory.subscribeToEvent("Evento","FrontTactilTouched","FrontTactilTouched")

    while 1:
        rbp=memory.getData("FrontTactilTouched")
        if rbp==1.0:
            print rbp
            talker("seal")
            time.sleep(3)
        print rbp

    memory.unsubscribeToEvent("Evento","FrontTactilTouched")
    sensor.unsubscribe("myApplication")

if __name__ == "__main__":
    robotIp = "148.226.225.217"
    robotPort = 9559
    main(robotIp,robotPort)