#!/usr/bin/env python
# Lo de arriba es una variable del sistema....No mover
# Librerias de ROS...Para comunicar nodos
import rospy
from std_msgs.msg import String
# Libreras del sistema, NAOQI, matematicas y tiempo
import sys
import motion
import time
import math
from naoqi import ALProxy

def callback(data):
    print "Entro al callback"
    c=data.data

    if c[0]!='5':
        c = [int(i) for i in c[1:-1].split(",")]

    if c[0]==1:
        print "Pararse"
        Stiffness(motionProxy,1)
        Posture(postureProxy,"StandInit",1)

    if c[0]==2:
        print "Sentarse"
        Posture(postureProxy,"Sit",1)
        Stiffness(motionProxy,0)

    if c[0]==3:
        print "Caminar"
        Caminar(motionProxy,c[1]/10.0,c[2]/10.0,c[3]/10.0,c[4]/10.0)
        if c[5]!=0:
            time.sleep(3)
            Detenerse(motionProxy)

    if c[0]==4:
        print "Mover Brazo"
        ArmL = [c[2], c[3], c[4], c[5], c[6]]
        Cuerpo(motionProxy,ArmL,c[1])

    if c[0]=='5':
        print "Hablar"
        tts.say(c[1:])

    if c[0]==6:
        print "Detenerse"
        Detenerse(motionProxy)

    if c[0]==7:
        print "Cambiar Pose"
        if c[1]==1:
            Posture(postureProxy,"Stand",1)
        if c[1]==2:
            Posture(postureProxy,"StandZero",1)
        if c[1]==3:
            Posture(postureProxy,"Crouch",1)
        if c[1]==4:
            Posture(postureProxy,"SitRelax",1)
        if c[1]==5:
            Posture(postureProxy,"LyingBelly",1) # No la hace
        if c[1]==6:
            Posture(postureProxy,"LyingBack",1) # No la hace

    if c[0]==8:
        print "Escucho"
        asr.setLanguage("English")
        vocabulary = ["hello", "my","name","is","kratos"]
        asr.setVocabulary(vocabulary, True)
        asr.subscribe("Test_ASR")
        time.sleep(20)
        asr.unsubscribe("Test_ASR")

    if c[0]==9:
        print "Mano"
        handName = ""        
        if c[1]==1:
            handName = 'RHand'
        else:
            handName = 'LHand'
        if c[2]==1:
            motionProxy.closeHand(handName)
        else:
            motionProxy.openHand(handName)

def listener():
    print "Entro al listener"
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("prueba", String, callback)
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
    # Define
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
 
    motionProxy.setWalkArmsEnabled(True, True) # Permite mover los brazos al mismo tiempo que camina (LeftArm,RightArm)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]]) # Activa los bumpers de los pies

    Stiffness(motionProxy,1) # Funcion para los motores...1 es encender
    Posture(postureProxy,"StandInit",1) # Llama a la funcion de posturas....nombre de postura + velocidad 0-1

    listener()

    postureProxy.goToPosture("Sit", 1) # Llama a la funcion de posturas....nombre de postura + velocidad 0-1
    Stiffness(motionProxy,0) # Funcion para los motores...0 es apagar

if __name__ == "__main__":
    robotIp = "192.168.1.102" #Direccion IP del NAO
    robotPort = 9559  # Puerto del NAO
    main(robotIp,robotPort)  # Llama a la funcion main()