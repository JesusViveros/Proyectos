#!/usr/bin/env python
import sys
import motion
import time
import math
from naoqi import ALProxy

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
    Stiffness(motionProxy,1)
    postureProxy.goToPosture(pose, velocity)

def Stiffness(proxy,x):
    pNames = "Body"
    pStiffnessLists = x
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def main(robotIP,robotPort):
    print "MAIN"
    global motionProxy
    global postureProxy
    global tts
    global tts
    try:
        motionProxy = ALProxy("ALMotion", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        #print "Error was: ", e
    print "ALMotion"
    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        #print "Error was: ", e
    print "ALRobotPosture"
    try:
        tts = ALProxy("ALTextToSpeech", robotIP, robotPort)
    except Exception,e:
        print "Could not create proxy to ALTextToSpeech"
        #print "Error was: ",e
    print "ALTextToSpeech"
    try:
        asr = ALProxy("ALSpeechRecognition", robotIP, robotPort)
    except Exception,e:
        print "Could not create proxy to ALSpeechRecognition"
        #print "Error was: ",e
    print "ALSpeechRecognition"
    try:
        memory = ALProxy("ALMemory",robotIp, robotPort)
    except Exception,e:
        print "Could not create proxy to ALSpeechRecognition"
        #print "Error was: ",e
    print "ALMemory"
    #tts.say("Ya casi")

    asr.getAudioExpression()

    #asr.setLanguage("Spanish")
    #vocabulary = ["si", "no", "Pararse", "Abajo"]
    #asr.setVocabulary(vocabulary, True)

    #asr.subscribe("Test_ASR")
    #print 'Speech recognition engine started'
    #time.sleep(10)
    #asr.unsubscribe("Test_ASR")
    #data = memory.getData("WordRecognized")
    #print "the data is"
    #print data
    #print( "data: %s" % data )
    
    print "FIN"
    #postureProxy.goToPosture("Crouch",1)
    #Stiffness(motionProxy,0)

if __name__ == "__main__":
    robotIp = "148.226.225.74"
    robotPort = 9559
    main(robotIp,robotPort)