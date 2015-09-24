#!/usr/bin/env python
import rospy
import std_msgs.msg as std

import sys
import motion
import time
from naoqi import ALProxy

def talker(val):
    pub = rospy.Publisher('Nao',std.String,queue_size=4)
    rospy.init_node('RVoz', anonymous=True)
    rate = rospy.Rate(10)
    pub.publish(val)
    rate.sleep()

def main(robotIP,robotPort):
    global asr
    global memory
    try:
        asr = ALProxy("ALSpeechRecognition", robotIP, robotPort)
    except Exception,e:
        print "Could not create proxy to ALSpeechRecognition"
    try:
        memory = ALProxy("ALMemory",robotIp, robotPort)
    except Exception,e:
        print "Could not create proxy to ALSpeechRecognition"

    asr.setLanguage("Spanish")

    vocabulary = ["Parate", "Sientate","Camina","Detente","Saluda","Salir","Levanta el brazo izquierdo"]
    asr.setVocabulary(vocabulary, True)
    
    asr.subscribe("ASR")
    memory.subscribeToEvent("SREvent","LastWordRecognized","LastWordRecognized")

    ant=[0,0]
    message=""
    while(1):
    	time.sleep(3)
        recolist=memory.getData("LastWordRecognized")
        print recolist
    
        if ant[0]==recolist[0]:
            continue
        elif recolist[0]=="Salir":
            break
        else:
            ant=recolist
            message=recolist[0]
            try:
                talker(message)
            except rospy.ROSInterruptException:
                print ""

    memory.unsubscribeToEvent("SREvent","LastWordRecognized")
    asr.unsubscribe("ASR")

if __name__ == "__main__":
    robotIp = "148.226.225.94"
    robotPort = 9559
    main(robotIp,robotPort)