#!/usr/bin/env python
#Ludovico enaudi
import rospy
from std_msgs.msg import String
import sys
import motion
import time
from naoqi import ALProxy

def callR(data):
    global band
    print "SR: callR"
    if band==False:
        band=True
        asr.setLanguage("Spanish")

        vocabulary = ["Parate", "Sientate","Camina","Detente","Saluda","Salir","Levanta el brazo izquierdo"]
        asr.setVocabulary(vocabulary, True)

        asr.subscribe("ASR")
        memory.subscribeToEvent("SREvent","LastWordRecognized","LastWordRecognized")
        ant=[0,0]
        message=""

        while(1):
            time.sleep(1.5)

            try:
                recolist=memory.getData("LastWordRecognized")
            except RuntimeError:
                print "Memoria Vacia"
                continue

            print recolist
            if ant[0]==recolist[0]:
                continue
            elif recolist[0]=="Salir":
                break
            else:
                ant=recolist
                message=recolist[0]
                talker(message)
            try:
                memory.removeData("LastWordRecognized")
            except RuntimeError:
                continue
    else:
        band=False
        memory.removeData("LastWordRecognized")
        memory.unsubscribeToEvent("SREvent","LastWordRecognized")
        asr.unsubscribe("ASR")

def listener():
    print "Entro al listener"
    rospy.init_node('listenerS', anonymous=True)
    rospy.Subscriber('Retroalimentacion',String, callR)
    rospy.spin()

def talker(val):
    pub = rospy.Publisher('RVoz',String,queue_size=4)
    rospy.init_node('RVoz', anonymous=True)
    rate = rospy.Rate(10)
    pub.publish(val)
    rate.sleep()

def main(robotIP,robotPort):
    global asr
    global memory
    global band
    band=False

    try:
        asr = ALProxy("ALSpeechRecognition", robotIP, robotPort)
    except Exception,e:
        print "Could not create proxy to ALSpeechRecognition"
    try:
        memory = ALProxy("ALMemory",robotIp, robotPort)
    except Exception,e:
        print "Could not create proxy to ALSpeechRecognition"

    listener()

if __name__ == "__main__":
    robotIp = "148.226.225.217"
    robotPort = 9559
    main(robotIp,robotPort)