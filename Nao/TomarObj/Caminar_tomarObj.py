from naoqi import ALProxy
import TrackNao as tn
import threading
import motion
import time
import math
import sys
import almath

def Bder():
    RightArmjoints = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll","RWristYaw"]

    ArmR=[80,-40,80,60,0]
    ArmR = [ x * motion.TO_RAD for x in ArmR]
    motionProxy.angleInterpolationWithSpeed(RightArmjoints, ArmR,0.1)

def Bizq():
    LeftArmjoints = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw"]

    ArmL=[80,30,-100,-60,0]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
    motionProxy.angleInterpolationWithSpeed(LeftArmjoints, ArmL,0.1)

    ArmL = [90,80,-90,-50,-80]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
#    motionProxy.angleInterpolationWithSpeed(LeftArmjoints, ArmL,0.1)
    motionProxy.closeHand("LHand")

    ArmL=[80,30,-100,-60,0]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
#    motionProxy.angleInterpolationWithSpeed(LeftArmjoints, ArmL,0.1)

def MoverBrazos():
    time.sleep(3)
    motionProxy.setWalkArmsEnabled(False,False)
    RightArmjoints = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll","RWristYaw"]
    LeftArmjoints = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll","LWristYaw"]
    ArmR=[80,-40,80,60,0]
    ArmR = [ x * motion.TO_RAD for x in ArmR]
    ArmL=[80,30,-100,-60,0]
    ArmL = [ x * motion.TO_RAD for x in ArmL]

    t = 0
    while (t<3):
        motionProxy.setAngles(LeftArmjoints,ArmL, 0.1)
#        motionProxy.setAngles(RightArmjoints,ArmR, 0.1)
        t = t + 0.2
        time.sleep(0.2)

    ArmL = [90,80,-90,-50,-80]
    ArmL = [ x * motion.TO_RAD for x in ArmL]

    t = 0
    while (t<3):
        motionProxy.setAngles(LeftArmjoints,ArmL, 0.1)
        t = t + 0.2
        time.sleep(0.2)

    ArmL=[80,30,-100,-60,0]
    ArmL = [ x * motion.TO_RAD for x in ArmL]
    t = 0
    while (t<3):
        motionProxy.setAngles(LeftArmjoints,ArmL, 0.1)
        t = t + 0.2
        time.sleep(0.2)

def Parar():
    motionProxy.stiffnessInterpolation("Body",1,1.0)
    postureProxy.goToPosture("StandInit",1)

def Sentar():
    postureProxy.goToPosture("Crouch",1)
    motionProxy.stiffnessInterpolation("Body",0,1.0)

def Caminar():
    motionProxy.setWalkTargetVelocity(0.6,0,0,0.1)

def Deternerse():
    motionProxy.setWalkTargetVelocity(0,0,0,0)

def main(robotIP,robotPort,url):
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


    # INICIAR CAMARA
    cam = tn.Cam(url)
    cam.move_camera()
    cam.start()


    # NO VA
    Parar()
    time.sleep(3)
    #a=[["LeftStepHeight", 0.005],["RightStepHeight", 0.005],["RightTorsoWx", -7.0*almath.TO_RAD],["TorsoWy", 5.0*almath.TO_RAD]]
    a=[["LeftStepHeight", 0.01],["RightStepHeight", 0.01]]
    motionProxy.move(0.01,0,0,a)
    #motionProxy.setWalkTargetVelocity(0.6,0,0,0.03)

    time.sleep(16)
    motionProxy.setWalkArmsEnabled(True,True)
    motionProxy.stopMove()
    # NO VA

    '''

    # PREPARARSE
    Parar()
    Caminar()
    time.sleep(8)

    # MOVIMIENTO
    motionProxy.setWalkArmsEnabled(False, False)
    motionProxy.openHand("LHand")
    #MoverBrazos()
    #Bizq()
    time.sleep(10)
#    motionProxy.setWalkArmsEnabled(True,True)
    '''

    # TERMINAR TODO
    Deternerse()
    Sentar()
    cam.end_cam()

if __name__ == "__main__":
    url = "http://192.168.0.100/image"
    #robotIp = "148.226.221.158"
    robotIp = "148.226.221.114"
    robotPort = 9559
    main(robotIp,robotPort,url)