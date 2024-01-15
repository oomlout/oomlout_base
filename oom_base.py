import time
import keyboard
import win32com.client
import pyautogui
import os

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
def mouse_move(x,y,dela=0):
    print(f"                Moving mouse to {x},{y}")
    pyautogui.moveTo(x, y)
    delay(dela)

def mouse_click(x,y,dela=0):
    print(f"                Clicking mouse at {x},{y}")
    pyautogui.click(x, y)
    delay(dela)

#keyboard

def send_keys_down(times=1,dela=0):
    send_keys_direction(direction="down",times=times,dela=0)

def send_keys_up(times=1,dela=0):
    send_keys_direction(direction="up",times=times,dela=0)

def send_keys_direction(direction,times=1,dela=0):
    print(f"            sending {direction} {times} times")
    for time in range(times):        
        pyautogui.press(direction)             
        delay(0.1)
    delay(dela)

def send_keys(string, **kwargs):
    dela = kwargs.get('dela', 0.1)
    count = kwargs.get('count', 1)  
    #if string is an int or float make it a string
    if isinstance(string, int) or isinstance(string, float):
        string = str(string)  
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

def send_keys_alt_tab(dela=1):
    print("                alt tab")
    pyautogui.keyDown('alt')
    delay(.15)
    pyautogui.press('tab')
    delay(.15)
    pyautogui.keyUp('alt')
    delay(.1)
    delay(dela)


def send_keys_ctrl(st, dela=0):
    print("                ctrl " + st)
    pyautogui.keyDown('ctrl')
    delay(.15)
    pyautogui.press(st)
    delay(.15)
    pyautogui.keyUp('ctrl')
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
        print(f"Generating {file_out}")
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
    git = kwargs.get('git', True)
    git_per = kwargs.get('git_per', 20000)
    filter = kwargs.get('filter', [""])

    #if filter isn't an array make it one
    if not isinstance(filter, list):
        filter = [filter]
    #go through all files in symbols/
    import os
    count = 1   
    count2 = 1
    for root, dirs, files in os.walk(directory):
        #for each directory
            for file in files:
                full_file = os.path.join(root, file )
                # if any of filter are in 
                if any(x in full_file for x in filter):
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
                            if count % git_per == 0:
                                import oom_kicad
                                if git:
                                    oom_kicad.push_to_git(count = count )
                count2 += 1
                #print a dot every 1000 files
                if count2 % 100000 == 0:
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
    symbol_name = symbol_name.replace('$', '_')
    symbol_name = symbol_name.replace('(', '_')
    symbol_name = symbol_name.replace(')', '_')
    symbol_name = symbol_name.replace('&', '_')
    symbol_name = symbol_name.replace('__', '_')
    symbol_name = symbol_name.replace('__', '_')
    symbol_name = symbol_name.replace('__', '_')
    symbol_name = symbol_name.replace('__', '_')
    return symbol_name

# label

import copy

def print_message_label(**kwargs):
    import multiprocessing
    target = print_message_label_task
    
    p = multiprocessing.Process(target=target, kwargs=kwargs)
    p.start()

def print_message_label_task(**kwargs):
    p3 = copy.deepcopy(kwargs)        
    file_output = make_message_label(**p3)
    p3["file_input"] = file_output
    print_pdf(**p3)
    pass
    
def make_message_label(**kwargs):
    import time
    file_template = "templates/template_label_message_76_mm_x_50_mm.svg.j2"
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    import random
    random_extra = str(random.randint(100000, 999999))

    file_output = f"output/label_{timestamp}_{random_extra}.svg"
    kwargs["file_output"] = file_output
    kwargs["file_template"] = file_template
    kwargs["file_output"] = file_output
    kwargs["dict_data"] = copy.deepcopy(kwargs)
    get_jinja2_template(**kwargs)
    file_output = convert_svg_to_pdf(file_input=file_output)
    return file_output

#ghostprint

def print_pdf(**kwargs):
    file_input = kwargs.get("file_input","")
    multiple = kwargs.get("multiple",1)
    ##scale to fit notes https://stackoverflow.com/questions/7446552/resizing-a-pdf-using-ghostscript
        
    printer = "zephyr_mcpaper"    

    ghostScript = "gswin64C.exe"    
    silentLaunch = "silentCMD.exe"

    ghostOptions = " -sDEVICE=mswinpr2 -q -dNOPAUSE -dFITTED"
    ghostQuit = " -c quit"

    pdfFile = '"' + file_input + '"'
    printerString = ' -sOutputFile="%printer%' + printer + '"'

    executeString = silentLaunch + " " + ghostScript + ghostOptions + printerString + " -f " + pdfFile + ghostQuit 
    
    print(f"printing {multiple} times {file_input}"  )
    for x in range(int(multiple)):
        os.system(executeString)
        delay(0.25)
    delay(1)

def print_pdf_adobe(**kwargs):
    file_input = kwargs.get("file_input","")
    multiple = kwargs.get("multiple",1)
    ##scale to fit notes https://stackoverflow.com/questions/7446552/resizing-a-pdf-using-ghostscript
         

    acrobat = '"C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe"'
    parameters = "/t"
    
    pdfFile = '"' + file_input.replace("/","\\") + '"'
    executeString = f"{acrobat} {parameters} {pdfFile}"   
    
    print(f"printing {multiple} times {file_input}"  )
    for x in range(int(multiple)):
        #add cmd to the prompt
        #os.system("start cmd /c " + executeString)
        import subprocess
        #run as an independent process don't wait for it to finish 
        subprocess.Popen(executeString)

        
        

        
        delay(0.25)
    delay(1)


# inkscape
def convert_svg_to_pdf(**kwargs):
    inkscape = "inkscape.exe"
    file_input = kwargs.get("file_input","")
    file_output = kwargs.get("file_output","")
    if file_output == "":
        file_output = file_input.replace(".svg", ".pdf")
    import os
    os.system(f'{inkscape} --export-type="pdf" {file_input} --export-filename={file_output}')
    return file_output
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


def get_jinja2_template(**kwargs):
    file_template = kwargs.get("file_template","")
    file_output = kwargs.get("file_output","")
    directory = kwargs.get("directory","")
    dict_data = kwargs.get("dict_data",{})

    #add files to dict_data if directory != ""
    if directory != "":
        files = add_files_to_dict_data(directory=directory)
        dict_data["files"] = files

    markdown_string = ""
    #if file _temoplate doesn't exist
    if not os.path.isfile(file_template):
        file_template = os.path.join("c:/gh/oomlout_base", file_template)    
    file_template = file_template.replace("/", "\\")
    with open(file_template, "r") as infile:
        markdown_string = infile.read()
    ##### sanitize part
    import copy
    data2 = copy.deepcopy(dict_data)

    import jinja2    
    try:
        markdown_string = jinja2.Template(markdown_string).render(p=data2)
    except Exception as e:
        print(f"error in jinja2 template: {file_template}")
        print(e)
        markdown_string = "markdown_string_error"
    #make directory if it doesn't exist
    directory = os.path.dirname(file_output)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_output, "w", encoding="utf-8") as outfile:
        outfile.write(markdown_string)
        print(f"jinja2 template file written: {file_output}")

def add_files_to_dict_data(**kwargs):
    directory = kwargs.get("directory",os.getcwd())
    files = []    
    #get a list of recursive files
    import glob
    files = glob.glob(f"{directory}/**/*.*", recursive=True)
    #replace all \\ with /
    for i in range(len(files)):
        files[i] = files[i].replace("\\","/")
    #remove the directory from the file name
    # replace \\ with / in directory
    directory = directory.replace("\\","/")
    for i in range(len(files)):
        files[i] = files[i].replace(f"{directory}/","")
    import copy
    files2 = copy.deepcopy(files)
    return files2


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
