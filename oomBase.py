import win32com.client
import win32con
import win32api
import time
import os
import pyautogui
import subprocess
import win32clipboard
import datetime
import winsound
import string
import PIL
from pathlib import Path
#oomSendKey(string)
#oomSendKeyNoWait(string)
import re
import shutil
import requests
import zipfile
import glob
import keyboard
import webbrowser
from PIL import ImageGrab

priority  = 1000;

inkscapePath = '"C:\\Program Files\\Inkscape\\bin\\inkscape.exe"'
curaPath = '"C:\\Program Files\\Ultimaker Cura 4.8.0\\Cura.exe"'
notepadPath = "C:\\Program Files\\Notepad++\\notepad++.exe"
notepad86Path = "C:\\Program Files (x86)\\Notepad++\\notepad++.exe"
autoitPath = '"C:\\Program Files (x86)\\AutoIt3\\SciTE\\SciTE.exe"'
idlePath = "C:\\Users\\Stuart McFarlan\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\idlelib\\idle.pyw"
idlePath38 = "C:\\Users\\Stuart-McFarlan\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\idlelib\\idle.pyw"
idlePathLaser = "C:\\Users\\Grenrick-McFarlan\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\idlelib\\idle.pyw"
idlePathPeter = "idle.pyw"
adobePath = "C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe"
              ##"C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe\"
adobePathx64 = "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe"
vscPath2 = "Code"
vscPath = "Code"

######  Basic Routines

startTime = ""

def oomRuntime(mode=""):
    global startTime
    if mode == "start":
        startTime = time.time()
    else:
        return("Time to execute: " + str(round(time.time()-startTime)) + " sec")

def strBetween(string,start,end):
    return stringBetween(string,start,end)

pinger = 0
def ping(divider=100):
    global pinger
    pinger=pinger+1
    if pinger % divider == 0:
        print(".",end="")

def stringBetweenLines(string,start,end):
    lineBreak = "AAA78622LLL"
    string = string.replace("\n",lineBreak)
    string = string.replace("\r","")
    rv = stringBetween(string,start,end)
    rv = rv.replace(lineBreak,"\n")
    return rv
    
def stringBetween(string,start,end):
    #print(string)
    #start = start.replace("(","\)")
    #start = start.replace(")","\)")
    #end = end.replace("(","\)")
    #end = end.replace(")","\)")
    returnvalue = re.search(start + "(.*?)" + end ,string)
    #returnvalue = re.search('listingid="(.*)" ',string)
    if returnvalue == None:
        return ""
    else:
        rv = returnvalue.group(1)
        return rv

def stringsBetween(string,start,end):
    #print(string)
    returnvalue = re.findall(start + "(.*?)" + end ,string)
    #returnvalue = re.search('listingid="(.*)" ',string)
    return returnvalue

def makeFileSafe(outFile):
    safechars = string.ascii_lowercase + string.ascii_uppercase + string.digits + '.-'
    outFile = ''.join([c for c in outFile if c in safechars])
    return outFile

def delay(t, escape =True):
    oomDelay(t,escape)

def oomDelay(t,escape=True):
    obprint("                    Delaying: " + str(t),10000)
    if t > 9:
        if t == 50:
            c=0
        for u in range(t):
            print(">", end='',flush=True)
        print("")
    if t < 1:
        time.sleep(t)
    else:
        exit = False
        for x in range(int(t)):
            print(".", end='',flush=True)
            for y in range(9):
                time.sleep(.1)
                if escape:
                    if keyboard.is_pressed("s"):
                        print("Delay Escaped")
                        time.sleep(2)
                        exit = True
                        break
            if exit:
                break


        print()    

def obprint(message, priorityA=0):
    if(priorityA <= priority):
        print(message)
    

def beep():
    oomBeep()

def oomBeep():
    frequency = 500  # Set Frequency To 2500 Hertz
    duration = 500  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

###### Save Webpage

def saveWebpageManual(link,outfile):
    oomLaunchFolder(link)
    oomDelay(10)
    oomSendControl("u")
    oomDelay(10)
    oomSendControl("a")
    oomDelay(5)
    oomCopy()
    oomDelay(5)    
    result = oomGetClipboard()
    oomWriteToFile(outfile,result)
    oomSendControl("w")
    oomDelay(10)    
    oomSendControl("w")
    oomDelay(10)    
    
def oomSaveUrl(url,saveFile):
    r = requests.get(url, allow_redirects=True)
    open(saveFile, 'wb').write(r.content)

def oomUnzip(file_name,dir_name,deleteZip=False):
    zip_ref = zipfile.ZipFile(file_name) # create zipfile object
    zip_ref.extractall(dir_name) # extract file to dir
    zip_ref.close() # close file
    if deleteZip:
        os.remove(file_name) # delete zipped file    


######  Date routines

def oomGetDate():
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    current = now.strftime("%Y-%m-%d")
    return current


def oomGetTime():
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    current = now.strftime("%Y-%m-%d-%H-%M-%S")
    return current

def oomGetTimeCSV():
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    current = now.strftime("%Y-%m-%d %H:%M:%S")
    return current


######  Keyboard Macros


def oomSend(st,delay=0):
    oomSendKeys(st)
    oomDelay(delay)

def send(st):
    oomSendKeys(st)

def oomSendKeys(st):
    print("                Sending: " + str(st))
    
    #st = st.replace("}","").rpleace("{","")

    swaps = [")", "(", "+"]
    for swap in swaps:
        st = st.replace(swap,"{" + swap + "}")    
    oomSendKeysNoWait(st)
    time.sleep(0.1)

def oomSendKey(st):
    print("                Sending single key: " + str(st))
    pyautogui.press(st)
    oomDelay(0.5)


def oomSendKeysNoWait(st):
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys(st, 0)


def oomSendControl(st, delay=0):
    oomSendControlKey(st,delay)

def oomSendCtrl(st):
    oomSendControlKey(st)    

def sendCtrl(st):
    oomSendControlKey(st)    

def oomSendControlKey(st,delay=0):
    print("                Control " + st)
    pyautogui.keyDown('ctrl')
    oomDelay(.01)
    pyautogui.press(st)
    oomDelay(.01)
    pyautogui.keyUp('ctrl')
    oomDelay(.1)
    oomDelay(delay)

def oomSendAltKey(st, delay=0):
    print("                Alt " + st)
    pyautogui.keyDown('alt')
    oomDelay(.15)
    pyautogui.press(st)
    oomDelay(.15)
    pyautogui.keyUp('alt')
    oomDelay(.1)
    oomDelay(delay)

def oomSendShiftKey(st, delay=0):
    print("                shift " + st)
    pyautogui.keyDown('shift')
    oomDelay(.15)
    pyautogui.press(st)
    oomDelay(.15)
    pyautogui.keyUp('shift')
    oomDelay(.1)
    oomDelay(delay)


def oomSendWindowsKey(st):
    print("                Control " + st)
    pyautogui.keyDown('win')
    oomDelay(.1)
    pyautogui.press(st)
    oomDelay(.1)
    pyautogui.keyUp('win')
    oomDelay(.25)
    
    
def oomSendControlShiftKey(st):
    print("                Control Shift " + st)
    pyautogui.keyDown('ctrl')
    oomDelay(.1)
    pyautogui.keyDown('shift')
    oomDelay(.1)
    pyautogui.press(st)
    oomDelay(.1)
    pyautogui.keyUp('shift')
    oomDelay(.1)
    pyautogui.keyUp('ctrl')
    oomDelay(.25)



#special combos

    
def oomSendAltTab(tabs=1,delay=0):
    oomSendKeysAltTabs(tabs)
    oomDelay(delay)

def oomSendKeysAltTab(tabs=1):
    oomSendKeysAltTabs(tabs)
    
def oomSendKeysAltTabs(rep):
    print("            Alt Tab")
    pyautogui.keyDown('alt')
    oomDelay(.1)
    for x in range(0,rep):
        pyautogui.keyDown('tab')
        oomDelay(.1)
        pyautogui.keyUp('tab')
        oomDelay(.1)    
    pyautogui.keyUp('alt')
    oomDelay(0.1)

######  KEYBOARD SHORTCUTS

def oomSelectAll():
    print("            Select All")
    oomSendControlKey("a")

def oomSendTab(times=1,delay=0):
    print("            Tab")
    for time in range(times):
        pyautogui.press('tab')
        oomDelay(0.1)
    oomDelay(delay)

def oomSendShiftTab(times=1,delay=0):
    print("            Shift Tab " + str(times))
    for time in range(times):
        pyautogui.keyDown('shift')
        oomDelay(.1)    
        pyautogui.press('tab')
        pyautogui.keyUp('shift')
        oomDelay(.1)    
        oomDelay(0.1)
    oomDelay(delay)

def oomSendEsc(delay=0):
    print("            Escape")
    pyautogui.press('esc')
    oomDelay(0.1)
    oomDelay(delay)
    
def oomSendRight(times=1,delay=0):
    for time in range(times):
        print("            Right")
        pyautogui.press('right')
        oomDelay(0.1)
    oomDelay(delay)
        
def oomSendLeft(times=1,delay = 0):
    for time in range(times):
        print("            Left")
        pyautogui.press('left')
        oomDelay(0.1)
    oomDelay(delay)    

    
def oomSendUp(times=1,delay = 0):
    for time in range(times):
        print("            Up")
        pyautogui.press('up')
        oomDelay(0.1)
    oomDelay(delay)
        
def oomSendDown(times=1,delay=0):
    for time in range(times):
        print("            Down")
        pyautogui.press('down')             
        oomDelay(0.1)
    oomDelay(delay)

def enter():
       oomSendEnter()
    
def oomSendEnter(delay = 0,times = 1):
    print("            Enter")
    for time in range(times):
        pyautogui.press('enter')
        oomDelay(0.1)
    oomDelay(delay)
    
def oomSendDelete(times=1,delay=0):
    print("            Delete")
    for time in range(times):
        pyautogui.press('del')
        oomDelay(0.1) 
    oomDelay(delay)

def oomSendSpace():
    print("            Space")
    pyautogui.press('space')
    oomDelay(0.1)    
    
def oomSendMinus():
    print("            Delete")
    pyautogui.press('-')
    oomDelay(0.1)

def oomSendMaximize():
    print("            Maximize")
    oomSendWindowsKey('up')
    oomDelay(1)



######  Mouse Macros


def oomMouseMove(x=-1,y=-1,pos=[None,None],delay=0.5):
    
    if pos[0] != None:
        x = pos[0]
        y = pos[1]
    print("            Moving: x: " + str(x) + " y: " + str(y) )
    pyautogui.moveTo(x,y)
    oomDelay(delay)
    
def oomMouseDrag(x,y):
    print("            Dragging: x: " + str(x) + " y: " + str(y) )
    pyautogui.dragTo(x,y,button='left', duration=0.25)

def oomMouseDoubleClick(x=-1,y=-1,pos=[None,None]):
    oomMouseClick(x,y,pos)
    oomDelay(0.25)
    oomMouseLeft()

def oomMouseClick(x=-1,y=-1,pos=[None,None],delay=0):
    if x != -1 or pos[0] != None:
        oomMouseMove(x,y,pos)
    oomMouseLeft()
    oomDelay(delay)

def oomMouseClickDrag(x1,y1,x2,y2):
    oomMouseMove(x1,y1)
    oomDelay(0.5)
    oomMouseDrag(x2,y2)
    oomDelay(0.5) 

def oomMouseLeft():
    print("                Clicking ((LEFT))")
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    

def oomMouseRight(delay=0):
    print("                Clicking ((RIGHT))")
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0,0,0)
    oomDelay(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0,0,0)
    oomDelay(0.1)
    oomDelay(delay)

def oomMouseLeftDown():
    print("                Clicking ((LEFT DOWN))")
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)

def oomMouseLeftUp():
    print("                Clicking ((LEFT UP))")
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)    

def oomMouseScrollWheel(movement=0):
    print("                Scrolling Wheel ((" + str(movement) + "))")
    pyautogui.scroll(movement)  
    
######  Launch Routines

def oomLaunch(fileName, delay=0):
    launchString = fileName
    print("Launching: " + launchString)
    subprocess.run(launchString)
    oomDelay(delay)


def oomLaunchKicad():
    oomLaunchPopen('"C:/Program Files/KiCad/7.0/bin/kicad.exe"')

def oomLaunchEagle(file = ""):
    oomLaunchPopen('"C:/EAGLE 9.6.2/eagle.exe" ' + '"' + file + '"')


def oomLaunchCmd(filename):
    launchString = 'start cmd /K "' + filename + '"'
    print("            Launching CMD: " + launchString)    
    os.system(launchString)

def oomLaunchOpen(fileName, delay=0):
    launchString = fileName
    print("            Opening: " + launchString)
    os.startfile(launchString)

def oomLaunchPopen(fileName, delay=0):
    launchString = fileName
    print("Launching: " + launchString)
    subprocess.Popen(launchString)
    oomDelay(delay)

def oomLaunchPython(fileName):
    launchString = "python " + fileName
    print("Launching: " + launchString)
    subprocess.run(launchString)

def oomLaunchFolder(fileName, delay=0):
    os.system('start explorer "' + fileName + '"')
    oomDelay(delay)

def oomLaunchStart(fileName,delay=0):
    os.system('start "' + fileName + '"')
    oomDelay(delay)


def oomLaunchPython(fileName):
    os.system('start py "' + fileName + '"')

def oomLaunchInkscape(fileName):
    launchString = inkscapePath + " " + fileName
    print("Launching: " + launchString)
    subprocess.Popen(launchString)

def oomMakePDF(inFile,outFile):
    executeString = "inkscape.exe --export-pdf-version=1.4 --export-text-to-path --export-filename=\"" + outFile + "\" \"" + inFile + "\""
    print("                Converting to PDF: " + inFile)
    subprocess.call(executeString)

def oomMakePNG(inFile,outFile):
    executeString = "inkscape.exe --export-dpi=1200 --export-filename=\"" + outFile + "\" \"" + inFile + "\""
    print("                Converting to PNG: " + inFile)
    subprocess.call(executeString)

def oomScreenCapture(filename,crop=[None,None,None,None]):
    print("Saving Screenshot: " + filename)
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(filename)
    if crop[0] != None:
        im = PIL.Image.open(filename)
        im_crop = im.crop((crop[0],crop[1],crop[0]+crop[2],crop[1]+crop[3]))
        if os.path.isfile(filename):
            print("    removing: " + filename)
            os.remove(filename)
            delay(0.5)
        im_crop.save(filename)
        
def oomLaunchNotepad(fileName):
    launchString = notepadPath + " \"" + fileName + "\""
    if not os.path.exists(notepadPath):
        launchString = notepad86Path + " \"" + fileName + "\""
    print("Launching: " + launchString)
    subprocess.Popen(launchString)    

def oomLaunchWebsite(filename):
    if os.path.exists("C:/Program Files/Google/chrome/Application/Chrome.exe"):
        chrome_path = "C:/Program Files/Google/chrome/Application/Chrome.exe %s"
    else:
        chrome_path = "C:/Program Files (x86)/Google/chrome/Application/Chrome.exe %s"
    webbrowser.get(chrome_path).open(filename)

    
def oomEditPython(fileName):
    ##launchString = idlePathPeter + " " + fileName
    launchString = '' + vscPath + ' -n "' + fileName +'"'
    launchString = 'start cmd /K "' + launchString + '"'
    print("Launching Edit Python: " + launchString)    
    #subprocess.Popen(launchString)
    ##os.startfile(launchString)
    
    #subprocess.Popen(launchString, shell=True)
    os.system(launchString)
    #os.system(launchString)

def oomLaunchVisualStudioCode(fileName):
    oomEditPython(fileName)
    #launchString = vscPath + " " + fileName
    #print("Launching: " + launchString)
    #try:
    #    subprocess.Popen(launchString)
    #except:
    #    launchString = vscPath2 + " " + fileName
    #    subprocess.Popen(launchString)
    

def oomFileSearchAndReplace(inFile, outFile, find, replace):
    string = oomReadFileToString(inFile)
    string = oomStringSearchAndReplace(string,find,replace)
    oomWriteToFile(outFile,string,utf=False)

def oomStringSearchAndReplace(inString, find, replace):
    inString = inString.replace(find, replace)
    return inString




    
def oomPrintPDFAdobe(pdfFile):
    ##https://stackoverflow.com/questions/619158/adobe-reader-command-line-reference
    exPath = adobePath
    if not os.path.isfile(exPath):
        exPath = adobePathx64
    

    printString = "/t /h"
    executeString = "\"" + exPath + "\" " + printString + " \"" + pdfFile + "\""
    print("Printing PDF Adobe:  " + executeString)
    subprocess.Popen(executeString)
    delay(5)
    
    ##subprocess.call(executeString) ##wait to finish

def oomPrintPDF(pdfFile, printer="Zephyr-McPaper"):
    ##scale to fit notes https://stackoverflow.com/questions/7446552/resizing-a-pdf-using-ghostscript
    if printer == "Z":
        printer = "Zephyr-McPaper"

    if(printer == "Marty-McPaper"):
        oomPrintPDFMarty(pdfFile, printer=printer)
    else:
            
        ghostScript = "gswin64C.exe"

        
        silentLaunch = "silentCMD.exe"

        ghostOptions = " -sDEVICE=mswinpr2 -q -dNOPAUSE"
        ghostQuit = " -c quit"

        pdfFile = '"' + pdfFile + '"'
        printerString = ' -sOutputFile="%printer%' + printer + '"'



        executeString = silentLaunch + " " + ghostScript + ghostOptions + printerString + " -f " + pdfFile + ghostQuit 
        
        print("Printing PDF:  " + executeString)
        subprocess.Popen(executeString, shell=False)
        delay(1)

def oomPrintPDFMarty(pdfFile, printer="Marty-McPaper"):
    ##scale to fit notes https://stackoverflow.com/questions/7446552/resizing-a-pdf-using-ghostscript
    if printer == "Z":
        printer = "Zephyr-McPaper"
    ghostScript = "gswin64C.exe"

    
    silentLaunch = "silentCMD.exe"


    ghostOptions = ' -sDEVICE=mswinpr2 -sPAPERSIZE=hagaki  -dPDFFitPage -c """<</Orientation 3>> setpagedevice""" -q -dNOPAUSE'
    
    ghostQuit = " -c quit"

    pdfFile = '"' + pdfFile + '"'
    printerString = ' -sOutputFile="%printer%' + printer + '"'
    

    executeString = silentLaunch + " " + ghostScript + ghostOptions + printerString + " -f " + pdfFile + ghostQuit 
    
    print("Printing PDF:  " + executeString)
    subprocess.Popen(executeString, shell=False)
    delay(1)    


def oomCopy():
    oomSendCtrl('c')
    oomDelay(0.1)


def oomPaste():
    oomSendCtrl('v')
    oomDelay(0.1)    
    

def oomGetClipboard():
    win32clipboard.OpenClipboard()
    clip = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return clip

def oomClipboardSaveImage(filename):
    im = ImageGrab.grabclipboard()
    try:
        im.save(filename,'PNG')
    except:
        print("No image in clipboard")

def oomSetClipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()

######  File things

fileOut = ""

def oomOpenFileUtf(filename):
    global fileOut
    fileOut = open(filename, "w+",encoding="utf-8")
    
def oomAddToOpenFileUtf(line):
    global fileOut
    fileOut.write(line)

def oomCloseFileUtf():
    global fileOut
    fileOut.close()


def oomAddLineToFile(fileName, line):
    f = open(fileName, "a+")
    f.write(str(line) + "\n")
    f.close()



def oomAddLineToFileUtf(fileName, line):
    f = open(fileName, "a+",encoding="utf-8")
    f.write(str(line) + "\n")
    f.close()


def oomReadUrlToString(url):
    returnV = ""
    try:
        r = requests.get(url, allow_redirects=True)
        returnV = r.content
    except getopt.GetoptError as e:
        pass
        raise e
        #print("Web page not opened")        
    return returnV

def oomReadFileToString(fileName, encoding=""):
    returnV = ""
    try:
        if encoding != "":
            f = open(fileName, "r",encoding=encoding)
        else:
            f = open(fileName, "r")
        returnV = f.read()
        f.close()
    except Exception as e:
        #raise e
        pass
        #print("No Google Sheet File")        
    return returnV

def oomReadFileLine(fileName):
    returnV = ""
    try:
        f = open(fileName, "r")
        returnV = f.readline()
        f.close()
    except:
        pass
        #print("No Google Sheet File")        
    return returnV

import git

def oomGitPullNew(gitBase,directory,onlyCreate=False):   
    oomMakeDir(directory) 
    outDir = directory + gitBase.rsplit("/")[-1].replace(".git","")
    skips = ["https://github.com/adafruit/adafruit-rpi-kernel.git"]
    if gitBase not in skips:
        if not os.path.isdir(outDir): ##### clone        
            print("        Git cloneing to: " + outDir )
            c = git.Repo.clone_from(gitBase, outDir)
            print("            CLONED!")      
        elif not onlyCreate: ###### pull
            print("        Git pulling to: " + outDir )
            g = git.cmd.Git(outDir)
            try:
                print(g.pull())
            except:
                print("Issue with git pull for: " + gitBase)
    return outDir    + "/"   
    
        



def oomGitPull(git,directory,close = True, pause = False):
    sp = git.split("/")
    repoName = sp[len(sp)-1]
    if repoName == "":
        repoName = sp[len(sp)-2]
    close = "/K"
    if not close:
        close = "/C"
    action = "pull"
    extra = repoName
    if repoName == "":
        raise Exception("No Repo Name Provided.")
    if not os.path.isdir(directory + repoName):
        action = "clone"
        extra = ""
    #cd sourceFiles/git/ && git pull https://github.com/electrolama/zig-a-zig-ah
    launchString = 'cd "' + directory + extra + '" &&'

    launchString = launchString + "git " + action + " " + git 
    if pause:
        launchString = launchString + "&& PAUSE "
    launchString = launchString +  " && EXIT"
    launchString = 'start /wait cmd ' + close + ' "' + launchString + '"'
    print("            Git Pull: " + launchString)    
    os.system(launchString)

def oomWriteToFileUtf(fileName, line):
    directory = os.path.dirname(fileName)
    oomMakeDir(directory)
    f = open(fileName, "w+", encoding="utf-8")
    f.write(line)    
    f.close()



def oomWriteToFile(fileName, line, utf=False, utf2=False):
    ##line = line.encode("utf_8", "ignore")
    directory = os.path.dirname(fileName)
    if directory != "" and not os.path.isdir(directory):
        os.mkdir(directory)
    f = open(fileName, "w+")
    if utf:
        f.write(str(line.encode('utf8')).replace("\\r\\n","\r\n"))    
    if utf2:
        f.write(str(line.encode('utf8')).replace("\\n","\u000A").replace("\\'","'").replace("b'","").replace("\u000A'",""))            
    else:
        try:
            f.write(line)    
        except:
            #wait = input("oomWriteToFile Error (Usually a unicode thing)")
            line = line.encode('ascii', "ignore")
            line = line.decode()
            f.write(line)
            #raise Exception("oomWriteToFile Error (Usually a unicode thing)")
    f.close()

def oomAddToFile(fileName, line, utf=False):
    ##line = line.encode("utf_8", "ignore")
    directory = os.path.dirname(fileName)
    if not os.path.isdir(directory):
        os.mkdir(directory)
    f = open(fileName, "a+")
    if utf:
        f.write(str(line.encode('utf8')).replace("\\r\\n","\r\n"))    
    else:
        f.write(line)    
    f.close()


def oomMakeDir(dir):
    Path(dir).mkdir(parents=True, exist_ok=True)

from distutils.dir_util import copy_tree

def oomCopyDir(src,dst):
    oomMakeDir(src)
    copy_tree(src,dst)

def oomCopyFile(src, dst):
    shutil.copyfile(src, dst)

def oomDeleteFile(file):
    if os.path.exists(file):
        print("    Deleting: " + file)
        os.remove(file)
    else:
        print("    File does not exist: " + file)

def oomDeleteDirectory(dir, safety=True):
    if safety:
        input("Deleting :" + dir + " (any key to continue, kill program to cancel)")
    else:
        print("Deleting :" + dir)
    if os.path.isdir(dir):    
        files = os.listdir(dir)
        for f in files:
            if os.path.isfile(dir + f):
                os.remove(dir + f)
        os.rmdir(dir)

######  Debug Things

def oomPrintVariables(values):
    for name, value in values:
        print(name, value)

###### CSV

import csv

def oomDictToCsv(filename,dic):
    f = open(filename,mode = "w+",encoding = "utf-8")    
    first = dic[0]
    csvF = csv.DictWriter(f,first.keys(),lineterminator="\n")
    csvF.writeheader()
    csvF.writerows(dic)
    f.close()

######  3 D printing

def oomSlice():
    oomSendCtrl("r")
    delay(10)
    oomSendCtrl("g")
    delay(2)
    oomSend("C:\\DB")
    delay(1)
    oomSendEnter()
    delay(1)
    oomSend("C:\\DB\\Dropbox\\BBBB-Product Working\\3DPR\\3DPR-SDCard\\temp")
    oomSendEnter()
    delay(1)
    oomSendEnter()
    delay(1)
    oomSend("y")

def oomOpenSlicer():
    os.system('start prusaslicer-updater.exe /silent -restartapp prusa-slicer.exe -startappfirst')
    delay(20)
    
