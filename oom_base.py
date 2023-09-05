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
#mouse
def move_mouse(x,y,dela=0):
    print(f"                Moving mouse to {x},{y}")
    pyautogui.moveTo(x, y)
    delay(dela)

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
    return_value  = 0
    filename = kwargs['filename']
    resolution = kwargs['resolution']
    overwrite = kwargs.get('overwrite', False)
    file_out = filename.split(".")[0] + "_" + str(resolution) + "." + filename.split(".")[1]
    #skip if overwrite is false and the file already exists
    if not overwrite:
        if os.path.isfile(file_out):
            return 0
    
    #if the image is already a resized on skip it chjeck for all numbers 100 or more
    if "_" in filename:
        if filename.split("_")[-1].split(".")[0].isdigit():
            if int(filename.split("_")[-1].split(".")[0]) >= 100:
                return 0
    
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
        return_value = 1
    except:
        print("Error with image: " + filename)
        pass
        return_value = 0
    return return_value

# do all image resolutions for a directory
def image_resolutions_dir(**kwargs):
    overwrite = kwargs.get('overwrite', False)
    directory = kwargs.get('directory', "")
    #go through all files in symbols/
    import os
    count = 1   
    count2 = 1
    for root, dirs, files in os.walk(directory):
        #for each directory
            for file in files:
                #if kicad_mod file
                if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                    resolutions = [140,300,600,1000]
                    filename = os.path.join(root, file )
                    #print(f"Generating images for {filename}")
                    for resolution in resolutions:
                        #generate the image at this resolution
                        
                        #print(filename)
                        counter = generate_image(filename=filename, resolution=resolution, overwrite=overwrite)
                        pass
                    if counter == None:
                        counter = 0
                        count += counter
                        #print a dot every 1000 files
                        if count % 100 == 0:
                            print("-", end="", flush=True)
                        #git commit every 5000 files
                        if count % 500 == 0:
                            import oom_kicad
                            oom_kicad.push_to_git(count = count )
                count2 += 1
                #print a dot every 1000 files
                if count2 % 1000 == 0:
                    print(".", end="", flush=True)
                    


def image_svg_to_png(**kwargs):
    filename = kwargs.get('filename', "")
    file_out = filename.replace(".svg", ".png")
    import os
    #convert with os.systyem call to inkscape
    print(f"Converting {filename} to {file_out}")
    os.system(f'inkscape --export-type="png" -w 2000 {filename}')


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


#git stuff

def git_clone(**kwargs):
    url = kwargs.get('url', "")
    if url != "":
        repo_name = kwargs.get('repo_name',"")
        if repo_name == "":
            #get repo name from url
            url_git = url
            if not url_git.endswith(".git"):
                url_git += ".git"
            repo_name = url_git.split("/")[-1].split(".")[0]
        #add repo name to fodler
        folder = kwargs.get('folder', "") + "/" + repo_name
        os.system("git clone " + url + " " + folder)
        return folder

def git_delete(**kwargs):
    url = kwargs.get('url', "")
    if url != "":
        repo_name = kwargs.get('repo_name',"")
        if repo_name == "":
            #get repo name from url
            url_git = url
            if not url_git.endswith(".git"):
                url_git += ".git"
            repo_name = url_git.split("/")[-1].split(".")[0]
        #add repo name to fodler
        folder = kwargs.get('folder', "") + "/" + repo_name
        if repo_name != "":
            print("Deleting " + folder)
            #replace / with \\
            folder = folder.replace("/","\\")
            os.system("rmdir /s /q " + folder)
