import os
import time
import keyboard
import win32com.client
import pyautogui

#timimng
def delay(t,escape=True):    
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

#keyboard
def send_keys(string, **kwargs):
    dela = kwargs.get('dela', 0.1)
    count = kwargs.get('count', 1)    
    print(f"                Sending: {str(string)}   {count} times with a delay of {dela}")    
    for x in range(count):
        #st = st.replace("}","").rpleace("{","")

        swaps = [")", "(", "+"]
        for swap in swaps:
            st = string.replace(swap,"{" + swap + "}")    
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys(string, 0)
        delay(dela)

def send_keys_alt(st, dela=0):
    print("                Alt " + st)
    pyautogui.keyDown('alt')
    delay(.15)
    pyautogui.press(st)
    delay(.15)
    pyautogui.keyUp('alt')
    delay(.1)
    delay(dela)

def send_enter(dela = 0,times = 1):
    print("            Enter")
    for time in range(times):
        pyautogui.press('enter')
        delay(0.1)
    delay(dela)

def send_esc(dela = 0,times = 1):
    print(f"            Esc {times} times")
    for time in range(times):
        pyautogui.press('esc')
        delay(0.1)
    delay(dela)

def send_tab(times=1,dela=0):
    print("            Tab")
    for time in range(times):
        pyautogui.press('tab')
        delay(0.1)
    delay(dela)

def send_tab_shift(times=1,dela=0):
    print("            Tab")
    for time in range(times):
        pyautogui.keyDown('shift')
        delay(.15)
        pyautogui.press('tab')
        delay(.15)
        pyautogui.keyUp('shift')
        delay(.1)
    delay(dela)


#image manipulation
def generate_image(**kwargs):
    filename = kwargs['filename']
    resolution = kwargs['resolution']
    overwrite = kwargs.get('overwrite', False)
    file_out = filename.split(".")[0] + "_" + str(resolution) + "." + filename.split(".")[1]
    #skip if overwrite is false and the file already exists
    if not overwrite:
        if os.path.isfile(file_out):
            return
    
    #if the image is already a resized on skip it chjeck for all numbers 100 or more
    if "_" in filename:
        if filename.split("_")[-1].split(".")[0].isdigit():
            if int(filename.split("_")[-1].split(".")[0]) >= 100:
                return
    
    #open the image file png or jpg
    from PIL import Image
    try:
        im = Image.open(filename)
        #scale the image so the largest side is reolution pixels wide
        width, height = im.size
        if width > height:
            scale = resolution / width
        else:
            scale = resolution / height
        new_width = int(width * scale)
        new_height = int(height * scale)
        im = im.resize((new_width, new_height), Image.ANTIALIAS)
        #save the image
        im.save(file_out)
    except:
        print("Error with image: " + filename)
        pass

# string manipulation

def remove_special_characters(string):
    symbol_name = string
    symbol_name = symbol_name.replace('/', '_')
    symbol_name = symbol_name.replace('\\', '_')
    symbol_name = symbol_name.replace(':', '_')
    symbol_name = symbol_name.replace('*', '_')
    symbol_name = symbol_name.replace('?', '_')
    symbol_name = symbol_name.replace('"', '_')
    symbol_name = symbol_name.replace('<', '_')
    symbol_name = symbol_name.replace('>', '_')
    symbol_name = symbol_name.replace('|', '_')
    symbol_name = symbol_name.replace('-', '_')        
    symbol_name = symbol_name.replace('+', '_')
    symbol_name = symbol_name.replace(' ', '_')
    symbol_name = symbol_name.replace('.', '_')
    symbol_name = symbol_name.replace('__', '_')
    symbol_name = symbol_name.replace('__', '_')
    symbol_name = symbol_name.replace('__', '_')
    symbol_name = symbol_name.replace('__', '_')
    return symbol_name




# data manipulation

#yaml to readme
def yaml_to_markdown(**kwargs):
    readme = ""
    yaml_dict = kwargs['yaml_dict']
    #if yaml_dict is an array take element 
    if type(yaml_dict) is list:
        yaml_dict = yaml_dict[0]
    #make a table with each yaml value key as a column value as the other
    #add header
    readme += "| Key | Value |  \n"
    readme += "| --- | --- |  \n"
    for key in yaml_dict:
        readme += "| " + key + " | " + str(yaml_dict[key]) + " |  \n"
        

    return readme