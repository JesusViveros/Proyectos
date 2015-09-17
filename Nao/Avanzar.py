#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import sys
import motion
import time
import math
from naoqi import ALProxy

def Girar(x):
    print "gira"
    Caminar(motionProxy,0.0,0.0,0.45*x,0.3)
    time.sleep(5)
    Caminar(motionProxy,0,0,0,0)

def Avanzar():
    print "Avanza"
    Caminar(motionProxy,0.8,0,0,0.2)
    time.sleep(6)

def Arrivar():
    orientation='N'
    ant='n'
    m=0
    for line in open("2Dpoints"):
        print "                   FOR"
        a=[int(i) for i in line[1:-2].split(",")]
        if ant=='n':
            print "ant=='n'"
            ant=a
            continue
        print "ant: "+str(ant)+" a: "+str(a)+" m: "+str(m)
        band=False
        if a[m]==ant[m]:
            print "a[m]==ant[m]"
            band=True
            if m==0:
                m=1
                print "M==1"
            else:
                m=0
                print "M==0"

        if a[m]>ant[m] and band==True:
            print "a[m]>ant[m]"
            if orientation=='N':
                print "orientation=='N'"
                orientation='D'
                Girar(1)
            elif orientation=='D':
                print "orientation=='D'"
                orientation='S'
                Girar(1)
            elif orientation=='S':
                print "orientation=='S'"
                orientation=='D'
                Girar(-1)
        ant=a
        Avanzar()

def Caminar(motionProxy,X,Y,Theta,Frequency):
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def main(robotIP,robotPort):
    global motionProxy
    global postureProxy
    try:
        motionProxy = ALProxy("ALMotion", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"

    motionProxy.setWalkArmsEnabled(True, True)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    motionProxy.stiffnessInterpolation("Body",1,1.0)
    postureProxy.goToPosture("StandInit",1)

    Arrivar()
    #Girar(1)
    #Avanzar()
    Caminar(motionProxy,0,0,0,0)

    postureProxy.goToPosture("Crouch",1)
    motionProxy.stiffnessInterpolation("Body",0,1.0)

if __name__ == "__main__":
    robotIp = "192.168.1.104"
    robotPort = 9559
    main(robotIp,robotPort)
    #Arrivar()
