#!/usr/bin/env python
# Lo de arriba es una variable del sistema....No mover
# Librerias de ROS...Para comunicar nodos
import rospy
from std_msgs.msg import String
from nao.msg import naomss
# Libreras del sistema, NAOQI, matematicas y tiempo
import sys
import motion
import time
import math
from naoqi import ALProxy

def callbackRV(data):
    print "Entro al callbackRV"
    c=data.data
    print c
    if c=="Parate":
        Stiffness(motionProxy,1)
        Posture(postureProxy,"StandInit",1)
    if c=="Sientate":
        Posture(postureProxy,"Crouch",1)
        Stiffness(motionProxy,0)
    if c=="Camina":
        Caminar(motionProxy,0.8,0.0,0.0,0.2)
    if c=="Detente":
        Detenerse(motionProxy)

def callbackSR(data):
    print "Entro al callbackSR"
    c=data.data
    if c=="ObsL":
        print "ObsL"
        Detenerse(motionProxy)
        Caminar(motionProxy,0.0,0.0,-0.5,0.2)
    if c=="ObsR":
        print "ObsR"
        Detenerse(motionProxy)
        Caminar(motionProxy,0.0,0.0,0.5,0.2)
    time.sleep(5)
    Detenerse(motionProxy)
    #Caminar(motionProxy,0.8,0.0,0.0,0.2)

def listener():
    print "Entro al listener"
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("RVoz", String, callbackRV)
    rospy.Subscriber("Sonar", String, callbackSR)
    rospy.spin()

def Cuerpo(motionProxy,ArmL,Part):
    HeadJoins = ["HeadPitch", "HeadYaw"]
    LeftArmjoints = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw"]
    RightArmjoints = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll","RWristYaw"]
    Pelvisjoints = ["RHipYawPitch", "LHipYawPitch"]
    LeftLegjoints = ["LHipPitch", "LHipRoll", "LKneePitch", "LAncklePitch","LAnckleRoll"]
    RightLegjoints = ["RHipPitch", "RHipRoll", "RKneePitch", "RAncklePitch","RAnckleRoll"]

    ArmL = [ x * motion.TO_RAD for x in ArmL]
    pFractionMaxSpeed = 0.2

    if Part==1:
        motionProxy.angleInterpolationWithSpeed(HeadJoins, ArmL, pFractionMaxSpeed)
    if Part==2:
        motionProxy.angleInterpolationWithSpeed(LeftArmjoints, ArmL, pFractionMaxSpeed)
    if Part==3:
        motionProxy.angleInterpolationWithSpeed(RightArmjoints, ArmL, pFractionMaxSpeed)
    if Part==4:
        motionProxy.angleInterpolationWithSpeed(Pelvisjoints, ArmL, pFractionMaxSpeed)
    if Part==5:
        motionProxy.angleInterpolationWithSpeed(LeftLegjoints, ArmL, pFractionMaxSpeed)
    if Part==6:
        motionProxy.angleInterpolationWithSpeed(LeftLegjoints, ArmL, pFractionMaxSpeed)

def Caminar(motionProxy,X,Y,Theta,Frequency):
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def Detenerse(motionProxy):
    X = 0.0
    Y = 0.0
    Theta = 0.0
    Frequency=0.0
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def Posture(postureProxy,pose,velocity):
    postureProxy.goToPosture(pose, velocity)

def Stiffness(proxy,x):
    pNames = "Body"
    pStiffnessLists = x
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def main(robotIP,robotPort):
    global motionProxy
    global postureProxy
    global tts
    try:
        motionProxy = ALProxy("ALMotion", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
    try:
        tts = ALProxy("ALTextToSpeech", robotIP, robotPort)
    except Exception,e:
        print "Could not create proxy to ALTextToSpeech"
    motionProxy.setWalkArmsEnabled(True, True)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    listener()

if __name__ == "__main__":
    robotIp = "148.226.221.134"
    robotPort = 9559
    main(robotIp,robotPort)