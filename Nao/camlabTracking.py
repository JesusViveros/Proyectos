import rospy
from std_msgs.msg import String
import cv2
import cv
import numpy as np
import urllib

# Se modifica el primer valor

def talker(val):
    pub = rospy.Publisher('RVision',String,queue_size=4)
    rospy.init_node('RVision', anonymous=True)
    rate = rospy.Rate(10)
    pub.publish(val)
    rate.sleep()

points =[]
fps = 25
capSize = (320,240) # this is the size of my source video
fourcc = cv2.cv.CV_FOURCC('X','V','I','D')

def url_to_image(url):
	resp = urllib.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	return image

izquierda = "http://192.168.0.100/command/ptzf.cgi?relative=0610"
derecha = "http://192.168.0.100/command/ptzf.cgi?relative=0410"
arriba = "http://192.168.0.100/command/ptzf.cgi?relative=0210"
abajo = "http://192.168.0.100/command/ptzf.cgi?relative=0810"
ArD = "http://192.168.0.100/command/ptzf.cgi?relative=0310"
ArI = "http://192.168.0.100/command/ptzf.cgi?relative=0110"
AbD = "http://192.168.0.100/command/ptzf.cgi?relative=0910"
AbI = "http://192.168.0.100/command/ptzf.cgi?relative=0710"
Wide = "http://192.168.0.100/command/ptzf.cgi?relative=1010"
Tele = "http://192.168.0.100/command/ptzf.cgi?relative=1110"
setting = "http://192.168.0.100/command/presetposition.cgi?HomePos"

url2 ="http://192.168.0.100/oneshotimage.jpg"

video = cv2.VideoWriter('output.avi',fourcc,fps,capSize)

def Contornos(thresh,frame):
        # find contours in the threshold image
        contours,_ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        # finding contour with maximum area and store it as best_cnt
        max_area = 0
        best_cnt = 1
        area = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                best_cnt = cnt

        # Encuentra el centroide de el cuerpo detectado
        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

        if (cx != 0):
            #print str(cx)+"  "+str(cy)
            points.append((cx,cy))

        w = len(points)

        #si no hay nada no guarda coordenadas (0,0)
        for i in range(0,w-1):
            cv2.line(frame,(points[i]),(points[i+1]),(255,0,0),2)
        return frame

def main():
    while True:
        image = url_to_image(url2)
        frame = cv2.flip(image,-1)
        frame = cv2.blur(frame,(3,3))

        # convert to hsv and find range of colors
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        cv2.line(frame,(0,120),(340,120),(0,255,0),1)

        #threshred = cv2.inRange(hsv,np.array((103,150, 150)), np.array((140,255,255)))
        threshred = cv2.inRange(hsv,np.array((0,0,0)), np.array((180,0,0)))
        #threshgreen = cv2.inRange(hsv,np.array((60,150,182)), np.array((72,171,222)))

        thresh2red = threshred.copy()
        #thresh2green = threshgreen.copy()

        frame=Contornos(threshred,frame)
        #frame=Contornos(threshred,frame)

        #video.write(image) 

        cv2.imshow('frame',frame)
        cv2.imshow('threshred',threshred)
        #cv2.imshow('threshgreen',threshgreen)

        tecla =cv2.waitKey(15)
        if (tecla>0):
            print tecla

        if (tecla==1048603):#Escape
            break

        if (tecla==1048695):#W
            content = urllib.urlopen(arriba).read()

        if (tecla==1048696):#X
            content = urllib.urlopen(abajo).read()

        if (tecla==1048673):#A
            content = urllib.urlopen(izquierda).read()

        if (tecla==1048676):#D
            content = urllib.urlopen(derecha).read()

        if (tecla==1048677):#E
            content = urllib.urlopen(ArD).read()

        if (tecla==1048689):#Q
            content = urllib.urlopen(ArI).read()

        if (tecla==1048675):#C
            content = urllib.urlopen(AbD).read()

        if (tecla==1048698):#Z
            content = urllib.urlopen(AbI).read()

        if (tecla==1048691):#S
            content = urllib.urlopen(Wide).read()

        if (tecla==1048694):#V
            content = urllib.urlopen(Tele).read()

if __name__ == '__main__':
    main()
    video.release()
    cv2.destroyAllWindows()