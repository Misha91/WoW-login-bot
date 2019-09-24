#   WoW Classic logging game screen detector (Python 3 + libs)
#   mikhail.ivanov@rocketmail.com


#   pip install opencv-python
import cv2

#   pip install numpy
import numpy as np
#   install tesseract using .exe installer + pip install pytesseract
#   https://github.com/UB-Mannheim/tesseract/wiki
import pytesseract
#   Set path from previous step


#pip install imutils
import imutils

#pip install Pillow
from PIL import Image, ImageFilter, ImageEnhance
from pytesseract import image_to_string

#pip install pyautogui
import pyautogui

import operator
import time
import random
from subprocess import Popen



login = ""
password = ""
acc = ""
server = ""
WOW_PATH = "C:\\Program Files (x86)\\World of Warcraft\\_classic_\\Wow.exe"
TES_PATH = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
USER = ""
MINDELAY = 50
MAXDELAY = 200
X_STEP_COEFF = 0.003
Y_STEP_COEFF = 0.025
X_RAND_COEFF = 0.01
Y_RAND_COEFF = 0.001
USER = 0

#pytesseract.pytesseract.tesseract_cmd = TES_PATH #r'C:\Program Files\Tesseract-OCR\tesseract.exe'

mainScreenWords = ['name', 'password', 'login']
accountsScreenWords = ['world', 'warcraft', 'accounts', 'wow 1', 'accept']
realmsScreenWords = ['german', 'realm', 'bloodfang', 'ashbringer', 'dreadmist', 'noggenfogger', 'medium']
queueScreenWords = ['change', 'realm', 'queue']
charScreenWords = ['delete', 'character', 'back', 'create', 'new']
discScreenWords = ['password', 'login', 'you', 'have', 'been', 'disconnected', 'server']
noIntScreen = ['you', 'have', 'been', 'disconnected', 'blz51901016']

scenes = {\
            0 : mainScreenWords,\
            1 : accountsScreenWords,\
            2 : realmsScreenWords,\
            3 : queueScreenWords,
            4 : charScreenWords, \
            5 : discScreenWords, \
            6 : noIntScreen \
        }


def getSceneId(scenes):
    text = getSceneText().lower()
    #print(text)

    probabilities = []
    for k in scenes.keys():
        prob = 0.0
        weight = 1 / len(scenes[k])
        for word in scenes[k]:
            if word in text: prob += weight
        probabilities.append(round(prob, 3))

    index, value = max(enumerate(probabilities), key=operator.itemgetter(1))

    #print(probabilities)
    #print(index, value)
    if (value > 0.5):
        return index
    else:
        return -1

def getSceneText():
    #Load img from folder
    #image = np.array(cv2.imread("5.png"))


    #Take screenshot
    image = np.array(pyautogui.screenshot())
    image = image[:, :, ::-1].copy()

    width, height = image.shape[:2]
    cntY, cntX = width//2, height//2
    minX, maxX, minY, maxY = int(cntX - 0.5*cntX), int(cntX + 0.5*cntX), int(cntY - 0.75*cntY), int(cntY + 0.9*cntY)

    #print(width, height)
    #print(cntX, cntY)
    #print(minX, maxX, minY, maxY)

    roi = image[minY:maxY, minX:]

    #cv2.imshow('1',roi)
    #cv2.waitKey(0)

    # get yellow text only
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (15, 190, 190), (36, 255,255))
    imask = mask>0
    res = np.zeros_like(roi, np.uint8)
    res[imask] = roi[imask]

    #cv2.imshow('2',res)
    #cv2.waitKey(0)

    #convert to grayscale and enhance
    img = cv2.cvtColor(np.array(res), cv2.COLOR_BGR2GRAY)
    kernel = np.ones((2, 2), np.uint8)
    roi = cv2.dilate(img, kernel, iterations=1)
    roi = cv2.erode(roi, kernel, iterations=1)

    #get text
    sceneText = (pytesseract.image_to_string(roi))
    #print(sceneText)

    #show image
    #cv2.imshow('3',roi)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return sceneText

def getWhiteSceneText():
    #Load img from folder
    #image = np.array(cv2.imread("t2.png"))


    #Take screenshot
    image = np.array(pyautogui.screenshot())
    image = image[:, :, ::-1].copy()

    width, height = image.shape[:2]
    cntY, cntX = width//2, height//2
    minX, maxX, minY, maxY = int(cntX - 0.5*cntX), int(cntX + 0.5*cntX), int(cntY - 0.75*cntY), int(cntY + 0.9*cntY)

    #print(width, height)
    #print(cntX, cntY)
    #print(minX, maxX, minY, maxY)

    roi = image[minY:maxY, minX:cntX]

    #cv2.imshow('1',roi)
    #cv2.waitKey(0)

    # get yellow text only
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 0, 210), (0, 0,255))
    imask = mask>0
    res = np.zeros_like(roi, np.uint8)
    res[imask] = roi[imask]

    #cv2.imshow('2',res)
    #cv2.waitKey(0)


    #convert to grayscale and enhance
    img = cv2.cvtColor(np.array(res), cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    roi = cv2.dilate(img, kernel, iterations=1)
    roi = cv2.erode(roi, kernel, iterations=1)

    #get text
    sceneText = (pytesseract.image_to_string(roi))
    #print(sceneText)

    #show image
    #cv2.imshow('3',roi)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return sceneText


def randomWait(a, b):
    sleepTime = round(random.randint(a*1000,b*1000)/1000, 2)
    print("Sleeping time: " + str(sleepTime))
    time.sleep(sleepTime)

def fakeDelay(a=MINDELAY, b=MAXDELAY):
    lwait = a
    hwait = b
    return round(random.randint(lwait,hwait)/1000, 3)

def enterCredentials(login, password):
    print("enter cred")
    if (USER == 1):
        pyautogui.hotkey('ctrl', 'a', interval=fakeDelay(300,800))
        pyautogui.press('del', interval=fakeDelay(300,800))
        for l in login:
            if (l.isupper()):
                pyautogui.press('capslock', interval=fakeDelay())
                pyautogui.press(l.lower(), interval=fakeDelay())
                pyautogui.press('capslock', interval=fakeDelay())
            else:
                pyautogui.press(l, interval=fakeDelay())

        pyautogui.press('tab', interval=fakeDelay())

    pyautogui.hotkey('ctrl', 'a', interval=fakeDelay(300,800))
    pyautogui.press('del', interval=fakeDelay(300,800))
    for p in password:
        if (p.isupper()):
            pyautogui.press('capslock', interval=fakeDelay())
            pyautogui.press(p.lower(), interval=fakeDelay())
            pyautogui.press('capslock', interval=fakeDelay())
        else:
            pyautogui.press(p, interval=fakeDelay())

    pyautogui.press('enter', interval=fakeDelay(300,800))
    print("exit cred")

def chooseAccount(acc):
    for k in acc:
        if (k == 'd'):
            pyautogui.press('down', interval=fakeDelay())
        if (k == 'u'):
            pyautogui.press('up', interval=fakeDelay())
    pyautogui.press('enter', interval=fakeDelay(300,800))

def chooseServer(server, servers):

    print("start choose")
    windowSize = pyautogui.size()
    xStep = int(windowSize[0] * X_STEP_COEFF)
    yStep =  int(windowSize[1] * Y_STEP_COEFF)
    xRand = int(windowSize[0] * X_RAND_COEFF)
    yRand = int(windowSize[1] * Y_RAND_COEFF)
    x = windowSize[0]//2 + random.randint(-xRand,xRand)
    y = 2*windowSize[1]//6 + random.randint(-yRand,yRand)
    #print(x,y)
    pyautogui.moveTo(x, y, duration = fakeDelay(600,1200))
    randomWait(0.5,0.7)
    pyautogui.click(x, y)
    randomWait(0.7,0.9)


    whiteText = getWhiteSceneText().lower()
    last = whiteText
    dir = -1
    while (not server in whiteText):
        x = x + random.randint(-xStep,xStep)
        y = y + dir*yStep + dir*random.randint(0,yRand)
        pyautogui.moveTo(x, y, duration = fakeDelay(400,800))
        pyautogui.click(x, y)
        time.sleep(0.5)
        whiteText = getWhiteSceneText().lower()
        canGo = True


        for s in servers.keys():
            if (not canGo): break
            for w in servers[s]:
                if w in whiteText:
                    whiteText = s.lower()
                    canGo = False
                    break

        if (canGo): whiteText = 'notfound'

        if (last == whiteText):
            dir = dir * (-1)
            x = windowSize[0]//2 + random.randint(-xRand,xRand)
            y = windowSize[1]//2 + random.randint(-yRand,yRand)

        last = whiteText
        print(last, dir)

    pyautogui.press('enter', interval=fakeDelay(300,800))
    print("exit choose")

def updateSettings():
    print("enter settings")
    fS = open("settings","r")
    fS = fS.readlines()
    global login, password, acc, server, WOW_PATH, \
        TES_PATH, MINDELAY, MAXDELAY, X_STEP_COEFF, \
        Y_STEP_COEFF, X_RAND_COEFF, Y_RAND_COEFF, USER

    login = (fS[0].split("login =")[1]).lstrip().rstrip()
    password = (fS[1].split("password =")[1]).lstrip().rstrip()
    acc = (fS[2].split("acc =")[1]).lstrip().rstrip()
    server = (fS[3].split("server =")[1]).lstrip().rstrip()

    WOW_PATH = (fS[4].split("WOW_PATH =")[1]).lstrip().rstrip()
    TES_PATH = (fS[5].split("TES_PATH =")[1]).lstrip().rstrip()
    MINDELAY = int((fS[6].split("MINDELAY =")[1]).lstrip().rstrip())
    MAXDELAY = int((fS[7].split("MAXDELAY =")[1]).lstrip().rstrip())
    X_STEP_COEFF = float((fS[8].split("X_STEP_COEFF =")[1]).lstrip().rstrip())
    Y_STEP_COEFF = float((fS[9].split("Y_STEP_COEFF =")[1]).lstrip().rstrip())
    X_RAND_COEFF = float((fS[10].split("X_RAND_COEFF =")[1]).lstrip().rstrip())
    Y_RAND_COEFF = float((fS[11].split("Y_RAND_COEFF =")[1]).lstrip().rstrip())
    USER = int((fS[12].split("USER =")[1]).lstrip().rstrip())
    pytesseract.pytesseract.tesseract_cmd = TES_PATH
    print("exit settings")

def idler():
    fS = open("settings","r")
    fS = fS.readlines()
    servers = {}
    for l in fS[13:]:
        tmp = (l.rstrip().lstrip()).split(' ')
        tmpList = []
        for w in tmp:
            tmpList.append(w.lower())
        servers[l.rstrip().lstrip()] = tmpList

    #print(servers)

    updateSettings()

    Popen([WOW_PATH])
    pyautogui.moveTo(int(pyautogui.size()[0]/2) + int(pyautogui.size()[0]/6), int(pyautogui.size()[1]/2), duration = fakeDelay(2000,4000))
    last = -1
    unknownCnt = 0
    while(True):
        state = getSceneId(scenes)
        print(state)

        if (state <= last and not (state == 3 or state == 4 or state == 5 or state == 6)): state = -1
        else:
            last = state
            unknownCnt = 0

        if (state == 0):
            enterCredentials(login, password)
            randomWait(0.5,1)
        elif (state == 1):
            chooseAccount(acc)
            randomWait(0.5, 1)
        elif (state == 2):
            chooseServer(server, servers)
            randomWait(1,3)
        elif (state == 3 or state == 4):
            if (state == 4):
                k = random.randint(0,10)
                if (k == 1):
                    pyautogui.press('down', interval=fakeDelay())
                if (k == 3):
                    pyautogui.press('up', interval=fakeDelay())
            randomWait(5, 10)
        elif (state == 5):
            randomWait(0.5,1)
            pyautogui.press('enter')
            randomWait(1,3)
            last = -1
        elif (state == 6):
            guiSize = pyautogui.size()
            x_cnt, y_cnt = int(11*guiSize[0]//20), int(515*guiSize[1]//1000)
            #print(guiSize, x_cnt, y_cnt)
            pyautogui.moveTo(x_cnt, y_cnt, duration = fakeDelay(1000, 3000))
            randomWait(0.5, 1)
            pyautogui.click(x_cnt, y_cnt)
            print("CLICKED ON BUTTON!")
            randomWait(0.5, 1)
            if (USER == 1):
                pyautogui.press('tab')
            last = -1
        else:
            print("WAITING STATE!")
            unknownCnt += 1
            if (unknownCnt >= 10):
                guiSize = pyautogui.size()
                x_cnt, y_cnt = int(guiSize[0]//2), int(guiSize[1]//2)
                print(guiSize, x_cnt, y_cnt)
                pyautogui.moveTo(x_cnt, y_cnt, duration = fakeDelay(1000, 3000))
                randomWait(0.5, 1)
                pyautogui.click(x_cnt, y_cnt)
                print("CLICKED ON CNT!")
                randomWait(0.5, 1)
                pyautogui.press('enter')
                unknownCnt = 0
                randomWait(0.5, 1)
                pyautogui.moveTo(int(pyautogui.size()[0]/2) + int(pyautogui.size()[0]/6), int(pyautogui.size()[1]/2), duration = fakeDelay(2000,4000))
                randomWait(0.5, 1)
            randomWait(1,3)


idler()
