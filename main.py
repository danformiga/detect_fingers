#Controle de mão robótica (InMoov) com OpenCV e Mediapipe
#Esse código permite a deteccao individual de cada dedo.
#Importar as bibliotecas OpenCV, MediaPipe e Serial.
#Descomente linhas 25 e 107 para habilitar comunicacao serial com arduino
#Autor: Daniel Formiga

import cv2
import time
import HTModule as htm
import serial
global ser

#Setup
PortaCam = 0 #Porta da Webcam - Normalmente 0 para WebCam integrada e 1 cameras USB.
PortaSerial = "COM8" #Porta Serial COM do Arduino
Baudrate = 115200 #Baudrate do Arduino

#Estado inicial
tstate = 0
istate = 0
pstate = 0
mstate = 0
rstate = 0
state = 6

wCam, hCam = 640, 480
#ser = serial.Serial(PortaSerial, Baudrate)
cap = cv2.VideoCapture(PortaCam)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

#Início da lógica de posicionamento
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    #print(lmList) #Debug matrizes

    if len(lmList) != 0:
        fingers = []
        # Lógica da localização e intertravamento com state
        #Intertravamento para não floodar a porta serial e travar
        # Polegar
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1] and tstate !=1:
            fingers.append(1)
            tstate = 1
            comando()
        elif lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1] and tstate !=0:
            fingers.append(0)
            tstate = 0
            comando()

        #Indicador
        if lmList[tipIds[1]][2] > lmList[tipIds[1] - 2][2] and istate != 0:
            fingers.append(1)
            istate = 0
            comando()
        elif lmList[tipIds[1]][2] < lmList[tipIds[1] - 2][2] and istate != 1:
            fingers.append(0)
            istate = 1
            comando()

        #Meio
        if lmList[tipIds[2]][2] > lmList[tipIds[2] - 2][2] and mstate != 0 :
            fingers.append(1)
            mstate = 0
            comando()
        elif lmList[tipIds[2]][2] < lmList[tipIds[2] - 2][2] and mstate != 1 :
            fingers.append(0)
            mstate = 1
            comando()

        #Anelar
        if lmList[tipIds[3]][2] > lmList[tipIds[3] - 2][2] and rstate != 0:
            fingers.append(1)
            rstate = 0
            comando()
        elif lmList[tipIds[3]][2] < lmList[tipIds[3] - 2][2] and rstate != 1:
            fingers.append(0)
            rstate = 1
            comando()

        #Mindinho
        if lmList[tipIds[4]][2] > lmList[tipIds[4] - 2][2] and pstate != 0:
            fingers.append(1)
            pstate = 0
            comando()
        elif lmList[tipIds[4]][2] < lmList[tipIds[4] - 2][2] and pstate != 1:
            fingers.append(0)
            pstate = 1
            comando()

        totalFingers = fingers.count(1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.imshow("Imagem", img)
    k = cv2.waitKey(10)
    if k == 27:  # Esc para sair
        break

    def comando(): #Escrita Serial
        #print(f'${pstate}{rstate}{mstate}{istate}{tstate}')
        string = "$" + str(int(pstate)) + str(int(rstate)) + str(int(mstate)) + str(int(istate)) + str(int(tstate))
       #ser.write(string.encode())  #DESCOMENTE PARA HABILITAR SERIAL
        print(f'Serial {string}')