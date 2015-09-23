#!/usr/bin/env python
import sys
import motion
import time
import math
from naoqi import ALProxy

def Stiffness(proxy,x):
    pNames = "Body"
    pStiffnessLists = x
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

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

def main(robotIP,robotPort):
    global motionProxy
    global postureProxy
    global tts
    global asr
    global memory
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
    try:
        asr = ALProxy("ALSpeechRecognition", robotIP, robotPort)
    except Exception,e:
        print "Could not create proxy to ALSpeechRecognition"
    try:
        memory = ALProxy("ALMemory",robotIp, robotPort)
    except Exception,e:
        print "Could not create proxy to ALSpeechRecognition"

    motionProxy.setWalkArmsEnabled(True, True)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    
    asr.setLanguage("Spanish")

    vocabulary = ["Derecha","Izuierda","Parate", "Sientate","Camina","Detente","Saluda","Salir","Levanta brazo izquierdo"]
    asr.setVocabulary(vocabulary, True)
    
    asr.subscribe("Test_ASR")
    memory.subscribeToEvent("Chuy","LastWordRecognized","LastWordRecognized")

    ant=[0,0]
    while(1):
    	time.sleep(3)
        recolist=memory.getData("LastWordRecognized")
        print recolist
    
        if ant[0]==recolist[0]:
            continue
        else:
            ant=recolist

        if recolist[0]=="Parate":
            postureProxy.goToPosture("StandInit", 1)
        elif recolist[0]=="Sientate":
            postureProxy.goToPosture("Crouch", 1)
        elif recolist[0]=="Camina":
            Caminar(motionProxy,0.8,0,0,0.2)
        elif recolist[0]=="Detente":
            Detenerse(motionProxy)
        elif recolist[0]=="Saluda":
            tts.say("hola")
        elif recolist[0]=="Levanta brazo izquierdo":
			Cuerpo(motionProxy,[-90,0,0,0,0],2)
        elif recolist[0]=="Derecha":
            Caminar(motionProxy,0,0,-0.5,0.2)
        elif recolist[0]=="izquierda":
            Caminar(motionProxy,0,0,0.5,0.2)
        elif recolist[0]=="Salir":
            tts.say("adios")
            break
    
    memory.unsubscribeToEvent("Chuy","LastWordRecognized")
    asr.unsubscribe("Test_ASR")

    postureProxy.goToPosture("Crouch", 1)
    Stiffness(motionProxy,0)

if __name__ == "__main__":
    robotIp = "148.226.225.94"
    robotPort = 9559
    main(robotIp,robotPort)