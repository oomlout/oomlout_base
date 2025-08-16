import pyautogui
import clipboard
import random
import time
import os
import sys

# Import platform-specific key detection modules
if sys.platform == "win32":
    import msvcrt
else:
    # For Linux/Mac, we'll use a simpler approach
    import select
    import tty
    import termios


def robo_chatgpt_prompt_type(**kwargs):
    position = kwargs.get('position', [0, 0])
    robo_mouse_click(position=position)

    prompt = kwargs.get('prompt', '')
    print(f"Typing the prompt:")
    pyautogui.typewrite(prompt, interval=0.025)
    time.sleep(1)
    #press enter to send the prompt
    print("Pressing enter...")
    pyautogui.press('enter')
    robo_delay(delay=40)

def robo_chrome_close_tab(**kwargs):
    delay = kwargs.get('delay', 1)
    #close the tab
    print("closing tab")
    pyautogui.hotkey('ctrl', 'w')
    robo_delay(delay=delay)

def robo_chrome_open_url(**kwargs):
    url = kwargs.get('url', '')
    delay = kwargs.get('delay', 1)
    message = kwargs.get('message', f"Opening the url: {url}...")
    #open the url in chrome
    print(message)
    os.system(f"start chrome {url}")
    robo_delay(delay=delay)


#corel things

def robo_corel_copy(**kwargs):
    delay = kwargs.get('delay', 1)
    copy_mode = kwargs.get('copy_mode', 'all')
    message = kwargs.get('message', f"Copying the selected items in Corel...")
    #copy the selected items in corel
    print(message)
    #press ctrl a
    if copy_mode == 'all':        
        robo_keyboard_press_ctrl_generic(string='a', delay=delay)
    #press ctrl c
    robo_keyboard_press_ctrl_generic(string='c', delay=delay)
    robo_delay(delay=delay)

def robo_corel_close_file(**kwargs):
    delay = kwargs.get('delay', 5)
    save_style = kwargs.get('save_style', "y")
    message = kwargs.get('message', f"Closing Corel...")
    #close corel
    print(message)
    #press alt_f
    robo_keyboard_press_alt_f(delay=5)
    #press c
    robo_keyboard_press_generic(string='c', delay=5)
    #if save_style is y then save the file    
    robo_keyboard_send(string=save_style, delay=2)
    #wait for the delay
    robo_delay(delay=delay)

def robo_corel_export_file(**kwargs):
    file_name = kwargs.get('file_name', '')
    file_type = kwargs.get('file_type', 'pdf')
    directory = kwargs.get('directory', '')
    if directory != '':
        file_name = os.path.join(directory, file_name)
    file_name_absolute = os.path.abspath(file_name)
    delay = kwargs.get('delay', 10)
    message = kwargs.get('message', f"Exporting the file: {file_name} as {file_type}...")
    print(message)
    #export the file in corel    
    if False:
        robo_keyboard_press_alt_f(delay=1)
        #send h twice
        robo_keyboard_press_generic(string='h', repeat=2, delay=1)
        #send enter
        robo_keyboard_press_enter(delay=1)
        #send filename absolute
        robo_keyboard_send(string=file_name_absolute, delay=2)
        #press enter to confirm
        robo_keyboard_press_enter(delay=2)
        #send y to overwrite
        robo_keyboard_send(string='y', delay=2)
        robo_delay(delay=delay)
    else:
        #select all
        robo_keyboard_select_all(delay=2)
        #send alt f
        robo_keyboard_press_alt_f(delay=1)
        #send e 
        robo_keyboard_press_generic(string='e', delay=20)
        # #send right
        # robo_keyboard_press_right(delay=2)
        # #send left
        # robo_keyboard_press_left(delay=2)
        #send tab
        #robo_keyboard_press_tab(delay=5, repeat=1)
        #mouse click because tab doesn't always work
        robo_mouse_click(position=[200, 429], delay=3)
        robo_mouse_click(position=[200, 429], delay=3)
        #send file type
        robo_keyboard_send(string=file_type, delay=5)
        #send enter
        robo_keyboard_press_enter(delay=5)      
        
        #sent shift tab once
        robo_keyboard_press_tab_shift(delay=2, repeat=1)
        #send file name absolute
        #send filename absolute
        robo_keyboard_send(string=file_name_absolute, delay=5)
        

        #press enter to confirm
        robo_keyboard_press_enter(delay=2)
        #send y to overwrite
        robo_keyboard_send(string='y', delay=5)
        #press enter to confirm
        robo_keyboard_press_enter(delay=5)
        
        robo_delay(delay=delay)

        

def robo_corel_open(**kwargs):
    file_name = kwargs.get('file_name', '')
    directory = kwargs.get('directory', '')
    if directory != '':
        file_name = os.path.join(directory, file_name)
    delay = kwargs.get('delay', 45)
    message = kwargs.get('message', f"Opening the file: {file_name}...")
    #open the file in corel
    print(message)
    #os.system(f"start CorelDRW {file_name}")
    #os.system(f'start {file_name}')
    os.system(f'start "" "{file_name}"')
    robo_delay(delay=delay)


def robo_corel_import_file(**kwargs):
    file_name = kwargs.get('file_name', '')
    directory = kwargs.get('directory', '')
    x = kwargs.get('x', "")
    y = kwargs.get('y', "")
    width = kwargs.get('width', "")
    height = kwargs.get('height', "")
    max_dimension = kwargs.get('max_dimension', "")
    if directory != '':
        file_name = os.path.join(directory, file_name)
    file_name_absolute = os.path.abspath(file_name)
    delay = kwargs.get('delay', 10)
    message = kwargs.get('message', f"Importing the file: {file_name} at position {x}, {y} with size {width}x{height} and max dimension {max_dimension}...")
    print(message)
    #import the file in corel
    #press ctrl i
    robo_keyboard_press_ctrl_i(delay=10)
    #send file name absolute
    robo_keyboard_send(string=file_name_absolute, delay=2)
    #press enter to confirm
    robo_keyboard_press_enter(delay=5)
    #click in window
    robo_mouse_click(position=[300, 300], delay=5)
    robo_mouse_click(position=[300, 300], delay=5)
    #if x, y, width, height are all skipped then just return
    if x == "" and y == "" and width == "" and height == "" and max_dimension == "":

        return
    else:
        if x != "" or y != "":
            robo_corel_set_position(**kwargs)
        if width != "" or height != "" or max_dimension != "":
            robo_corel_set_size(**kwargs)

def robo_corel_paste(**kwargs):
    delay = kwargs.get('delay', 1)
    message = kwargs.get('message', f"Pasting the copied items in Corel...")
    x = kwargs.get('x', "")
    y = kwargs.get('y', "")
    width = kwargs.get('width', "")
    height = kwargs.get('height', "")
    max_dimension = kwargs.get('max_dimension', "")
    #paste the copied items in corel
    print(message)
    #press ctrl v
    robo_keyboard_press_ctrl_generic(string='v', delay=2)
    #if x, y, width, height are all skipped then just return
    if x != "" or y != "":
        robo_corel_set_position(x=x, y=y)
    if width != "" or height != "" or max_dimension != "":
        robo_corel_set_size(width=width, height=height, max_dimension=max_dimension, delay=2)
    robo_delay(delay=delay)

def robo_corel_save(**kwargs):
    message = kwargs.get('message', f"Saving the file")
    #save the file in corel
    print(message)
    #press ctrl s
    robo_keyboard_press_ctrl_generic(string='s', delay=10)


def robo_corel_save_as(**kwargs):
    
    filename = kwargs.get('file_name', '')
    directory = kwargs.get('directory', '')

    if directory != '':
        filename = os.path.join(directory, filename)
    filename_absolute = os.path.abspath(filename)
    message = kwargs.get('message', f"Saving the file {filename_absolute}")
    #save the file in corel
    print(message)
    #move back and forth to enable the save so it's always six
    #select all
    if True:
        robo_keyboard_select_all(delay=1)
        #send left
        robo_keyboard_press_left(delay=1)
        #send right
        robo_keyboard_press_right(delay=1)
    
    #press alt f
    robo_keyboard_press_alt_f(delay=1)
    #press down 6 times
    robo_keyboard_press_down(delay=0.5, repeat=6)
    #press enter
    robo_keyboard_press_enter(delay=5)
    #send the file name
    robo_keyboard_send(string=filename_absolute, delay=5)
    #press enter to confirm
    robo_keyboard_press_enter(delay=5)
    #y to overwrite
    robo_keyboard_send(string='y', delay=5)
    #wait 20 seconds
    robo_delay(delay=20)

def robo_corel_trace(**kwargs):
    return robo_corel_trace_clipart(**kwargs)
    #return robo_corel_trace_lineart(**kwargs)

def robo_corel_trace_clipart(**kwargs):
    message = kwargs.get('message', f"tracing lineart")
    #trace the clipart in corel
    print(message)
    #press alt b
    robo_keyboard_press_alt_generic(string='b', delay=1)
    #press o
    robo_keyboard_send(string='o', delay=1)
    #press right
    robo_keyboard_press_right(delay=1)
    #press down 0 times
    robo_keyboard_press_down(delay=0.5, repeat=3)
    #press enter
    robo_keyboard_press_enter(delay=30)
    #909,568
    #click to reduce bitmap
    robo_mouse_click(position=[909, 568], delay=30)
    #all settings inherited    
    if False:
        #press tab 10 times
        robo_keyboard_press_tab(delay=0.5, repeat=10)
        #press space
        robo_keyboard_press_space(delay=1)
        #shift tab 6
        robo_keyboard_press_tab_shift(delay=0.5, repeat=6)
        #send ctrl select all
        robo_keyboard_press_ctrl_generic(string='a', delay=1)
        #send 10
        robo_keyboard_send(string='0', delay=20)
        #press shift tab 4 times
        robo_keyboard_press_tab_shift(delay=0.5, repeat=4)
        #press enter
    #click to set detail all but one 1337,366
    #all but one
    #robo_mouse_click(position=[1337, 366], delay=10)
    #max
    robo_mouse_click(position=[1348, 366], delay=30)
    robo_keyboard_press_enter(delay=30)

def robo_corel_trace_lineart(**kwargs):
    message = kwargs.get('message', f"tracing lineart")
    #trace the clipart in corel
    print(message)
    #press alt b
    robo_keyboard_press_alt_generic(string='b', delay=1)
    #press o
    robo_keyboard_send(string='o', delay=1)
    #press right
    robo_keyboard_press_right(delay=1)
    #press down 0 times
    #robo_keyboard_press_down(delay=0.5, repeat=3)
    #press enter
    robo_keyboard_press_enter(delay=30)
    #909,568
    #click to reduce bitmap
    robo_mouse_click(position=[909, 568], delay=30)
    #all settings inherited    
    if False:
        #press tab 10 times
        robo_keyboard_press_tab(delay=0.5, repeat=10)
        #press space
        robo_keyboard_press_space(delay=1)
        #shift tab 6
        robo_keyboard_press_tab_shift(delay=0.5, repeat=6)
        #send ctrl select all
        robo_keyboard_press_ctrl_generic(string='a', delay=1)
        #send 10
        robo_keyboard_send(string='0', delay=20)
        #press shift tab 4 times
        robo_keyboard_press_tab_shift(delay=0.5, repeat=4)
        #press enter
    #click to set detail all but one 1337,366
    robo_mouse_click(position=[1337, 366], delay=10)
    robo_keyboard_press_enter(delay=30)

def robo_corel_set_position(**kwargs):
    x = kwargs.get('x', "")
    y = kwargs.get('y', "")
    
    if x != "" and y != "":
        print(f"Setting the position to {x}, {y}")
        #send ctrl {enter}
        robo_keyboard_press_ctrl_enter(delay=1)
        #send tab
        robo_keyboard_press_tab(delay=0.5)
        robo_keyboard_send(string=str(x))
        robo_keyboard_press_tab(delay=0.5)
        robo_keyboard_send(string=str(y))
        #press enter
        robo_keyboard_press_enter(delay=0.5)

def robo_corel_set_size(**kwargs):
    width = kwargs.get('width', "")
    height = kwargs.get('height', "")
    max_dimension = kwargs.get('max_dimension', "")
    delay = kwargs.get('delay', 2)

    if width != "" and height != "":
        #set the size of the object        
        print(f"Setting the size to {width}x{height}")
        
        robo_keyboard_press_ctrl_enter(delay=1)
        #send tab 3 times
        robo_keyboard_press_tab(delay=0.5, repeat=3)
        #send width
        pyautogui.typewrite(f"{width}", interval=0.025)
        robo_keyboard_press_tab(delay=0.5)
        #send height
        pyautogui.typewrite(f"{height}", interval=0.025)
        robo_keyboard_press_enter(delay=0.5)
    elif width != "" or height != "":        
        #turn on the lock aspect ratio
        if True:            
            robo_keyboard_press_ctrl_enter(delay=1)
            #send tab 7 times
            robo_keyboard_press_tab(delay=0.5, repeat=7)
            # send space
            robo_keyboard_press_space(delay=0.5)
        robo_keyboard_press_ctrl_enter(delay=1)
        num_tabs = 3
        dimen = width
        if height != "":
            num_tabs = 4
            dimen = height
        robo_keyboard_press_tab(delay=0.5, repeat=num_tabs)
        #send dimension
        pyautogui.typewrite(f"{dimen}", interval=0.025)
        robo_keyboard_press_enter(delay=0.5)
        #turn off the lock aspect ratio
        if True:            
            robo_keyboard_press_ctrl_enter(delay=1)
            #send tab 7 times
            robo_keyboard_press_tab(delay=0.5, repeat=7)
            # send space
            robo_keyboard_press_space(delay=0.5)
    elif max_dimension != "":   
        #turn on the lock aspect ratio
        if True:            
            robo_keyboard_press_ctrl_enter(delay=1)
            #send tab 7 times
            robo_keyboard_press_tab(delay=0.5, repeat=7)
            # send space
            robo_keyboard_press_space(delay=0.5)     
        width_current = 0
        robo_keyboard_press_ctrl_enter(delay=1)
        #send tab 3 times
        robo_keyboard_press_tab(delay=0.5, repeat=3)
        try:
            width_current = float(robo_keyboard_copy(**kwargs).replace(" mm", ""))
        except Exception as e:
            print(f"Error reading width: {e}")
            width_current = 0
        #send tab 1 times
        robo_keyboard_press_tab(delay=0.5, repeat=1)
        try:
            height_current = float(robo_keyboard_copy(**kwargs).replace(" mm", ""))
        except Exception as e:
            print(f"Error reading height: {e}")
            height_current = 0

        if height_current > width_current:        
            #send max dimension
            robo_keyboard_send(string=str(max_dimension), delay=1)
        else:
            #send shift tab once
            robo_keyboard_press_tab_shift(delay=0.5, repeat=1)
            #send max dimension
            robo_keyboard_send(string=str(max_dimension), delay=1)
        #press enter
        robo_keyboard_press_enter(delay=0.5)
        #turn off the lock aspect ratio
        if True:            
            robo_keyboard_press_ctrl_enter(delay=1)
            #send tab 7 times
            robo_keyboard_press_tab(delay=0.5, repeat=7)
            # send space
            robo_keyboard_press_space(delay=0.5)

    robo_delay(delay=delay)
        

    

def robo_file_copy(**kwargs):

    method = kwargs.get('method', 'shutil')


    file_source = kwargs.get('file_source', '')
    file_destination = kwargs.get('file_destination', '')
    if file_source != "" and file_destination != "":
        if method == 'xcopy':
            #check if the file exists
            if os.path.isfile(file_source):        
                print(f"copying {file_source} to {file_destination}")
                #use xcopy with overwrite and no prompt
                os.system(f"xcopy {file_source} {file_destination} /Y /N /I")
            else:
                print(f"file {file_source} does not exist")
        elif method == 'shutil':
            #check if the file exists
            if os.path.isfile(file_source):
                print(f"copying {file_source} to {file_destination}")
                #use shutil to copy the file
                import shutil
                shutil.copy(file_source, file_destination)
            else:
                print(f"file {file_source} does not exist")


def robo_keyboard_close_tab(**kwargs):
    robo_chrome_close_tab(**kwargs)

def robo_keyboard_copy(**kwargs):
    delay = kwargs.get('delay', 1)
    position = kwargs.get('position', [0, 0])
    #click positionem of 
    if position != [0, 0]:
        pos = position
        pyautogui.click(pos[0], pos[1])
    #copy the text from the clipboard
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    #get the text from the clipboard
    clip = clipboard.paste()
    robo_delay(delay=delay)
    return clip

def robo_keyboard_press_alt_f(**kwargs):
    kwargs["string"] = "f"
    robo_keyboard_press_alt_generic(**kwargs)

def robo_keyboard_press_alt_generic(**kwargs):
    string = kwargs.get('string', '')
    delay = kwargs.get('delay', 1)
    delay_keypress = kwargs.get('delay_keypress', 0.025)
    repeat = kwargs.get('repeat', 1)
    #press ctrl + string
    if repeat > 1:
        print(f"pressing alt + {string} {repeat} times")
        for i in range(repeat):
            pyautogui.hotkey('alt', string)
            time.sleep(delay_keypress)
        robo_delay(delay=delay)
    else:
        print(f"pressing alt + {string} once")
        pyautogui.hotkey('alt', string)
        robo_delay(delay=delay)

def robo_keyboard_press_ctrl_generic(**kwargs):
    string = kwargs.get('string', '')
    delay = kwargs.get('delay', 1)
    delay_keypress = kwargs.get('delay_keypress', 0.025)
    repeat = kwargs.get('repeat', 1)
    #press ctrl + string
    if repeat > 1:
        print(f"pressing ctrl + {string} {repeat} times")
        for i in range(repeat):
            pyautogui.hotkey('ctrl', string)
            time.sleep(delay_keypress)
        robo_delay(delay=delay)
    else:
        print(f"pressing ctrl + {string} once")
        pyautogui.hotkey('ctrl', string)
        robo_delay(delay=delay)

def robo_keyboard_press_ctrl_enter(**kwargs):
    kwargs["string"] = "enter"
    robo_keyboard_press_ctrl_generic(**kwargs)


def robo_keyboard_press_ctrl_i(**kwargs):
    kwargs["string"] = "i"
    robo_keyboard_press_ctrl_generic(**kwargs)

#press esc
def robo_keyboard_press_escape(**kwargs):
    kwargs["string"] = "esc"
    robo_keyboard_press_generic(**kwargs)

#press down
def robo_keyboard_press_down(**kwargs):
    kwargs["string"] = "down"
    robo_keyboard_press_generic(**kwargs)

#press up
def robo_keyboard_press_up(**kwargs):
    kwargs["string"] = "up"
    robo_keyboard_press_generic(**kwargs)

#press left
def robo_keyboard_press_left(**kwargs):
    kwargs["string"] = "left"
    robo_keyboard_press_generic(**kwargs)

#press right
def robo_keyboard_press_right(**kwargs):
    kwargs["string"] = "right"
    robo_keyboard_press_generic(**kwargs)

#press enter
def robo_keyboard_press_enter(**kwargs):
    kwargs["string"] = "enter"
    robo_keyboard_press_generic(**kwargs)

#press space
def robo_keyboard_press_space(**kwargs):
    kwargs["string"] = "space"
    robo_keyboard_press_generic(**kwargs)

#press tab
def robo_keyboard_press_tab(**kwargs):
    kwargs["string"] = "tab"
    robo_keyboard_press_generic(**kwargs)

#press tab
def robo_keyboard_press_tab_shift(**kwargs):
    kwargs["string"] = "tab"
    robo_keyboard_press_shift_generic(**kwargs)

#press string
def robo_keyboard_send(**kwargs):
    robo_keyboard_press_string(**kwargs)
        
def robo_keyboard_press_string(**kwargs):
    string = kwargs.get('string', '')
    delay = kwargs.get('delay', 1)
    delay_keypress = kwargs.get('delay_keypress', 0.025)    
    print(f"pressing {string} once")
    pyautogui.typewrite(string, interval=delay_keypress)
    robo_delay(delay=delay)

def robo_keyboard_press_generic(**kwargs):
    string = kwargs.get('string', '')
    delay = kwargs.get('delay', 1)
    delay_keypress = kwargs.get('delay_keypress', 0.258)
    repeat = kwargs.get('repeat', 1)
    #press escape to close the menu
    if repeat > 1:
        print(f"pressing {string} {repeat} times")
        for i in range(repeat):
            pyautogui.press(string)
            time.sleep(delay_keypress)
        robo_delay(delay=delay)
    else:
        print(f"pressing {string} once")
        pyautogui.press(string)
        robo_delay(delay=delay)

def robo_keyboard_press_shift_generic(**kwargs):
    string = kwargs.get('string', '')
    delay = kwargs.get('delay', 1)
    delay_keypress = kwargs.get('delay_keypress', 0.258)
    repeat = kwargs.get('repeat', 1)
    #press escape to close the menu
    if repeat > 1:
        print(f"pressing shift {string} {repeat} times")
        for i in range(repeat):
            pyautogui.keyDown('shift')
            pyautogui.press(string)
            pyautogui.keyUp('shift')
            time.sleep(delay_keypress)
        robo_delay(delay=delay)
    else:
        print(f"pressing shift {string} once")
        pyautogui.keyDown('shift')
        pyautogui.press(string)
        pyautogui.keyUp('shift')
        robo_delay(delay=delay)


def robo_keyboard_select_all(**kwargs):
    delay = kwargs.get('delay', 1)
    #select all
    print("selecting all")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    robo_delay(delay=delay)

def check_key_pressed():
    """Check if any key is pressed and return it, or None if no key is pressed"""
    try:
        if sys.platform == "win32":
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                return key
        else:
            # For Linux/Mac - simplified approach
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                key = sys.stdin.read(1).lower()
                return key
    except Exception as e:
        # If key detection fails, just continue without it
        pass
    return None

def robo_delay(**kwargs):
    delay = kwargs.get('delay', 1)
    rand = kwargs.get('rand', 0)
    message = kwargs.get('message', f"")
    if message != "":
        print(f"message")
    if rand > 0:
        rand_amount = random.randint(0, rand)
        delay = delay + rand_amount
    if delay <= 1:
        time.sleep(delay)
    elif delay > 5:
        print(f"<<<<<>>>>> waiting for {delay} seconds (press 's' to skip) or turn scroll lock off")
    
        splits = 10
        for i in range(splits):
            #print the progress bar
            print(".", end='', flush=True)
            for i in range(int(delay/splits)):
                # Check if 's' key is pressed
                key = check_key_pressed()
                if key == 's':
                    print("\nDelay skipped by pressing 's' key")
                    time.sleep(1)
                    return
                #check scroll lock state
                import ctypes

                if ctypes.windll.user32.GetKeyState(0x91) & 1 == 1:
                    print("\Scroll Lock is OFF, skipping delay")
                    time.sleep(2)
                    pyautogui.press('scrolllock')
                    return
                time.sleep(1)
        print("")
    else:
        print(f"waiting for {delay} seconds (press 's' to skip)", end='', flush=True)
        for i in range(delay):
            #print the progress bar
            print(".", end='', flush=True)
            # Check if 's' key is pressed
            key = check_key_pressed()
            if key == 's':
                print("\nDelay skipped by pressing 's' key")
                time.sleep(5)
                return
            time.sleep(1)
        print("")

def robo_mouse_click(**kwargs):
    position = kwargs.get('position', [0, 0])
    delay = kwargs.get('delay', 1)
    button = kwargs.get('button', 'left')
    #click the mouse at the position
    print(f"Clicking at {position}...")
    pos = position
    pyautogui.click(pos[0], pos[1], button=button)
    robo_delay(delay=delay)

def robo_screenshot(**kwargs):
    position = kwargs.get('position', [0, 0])
    #if position is only two values add size to it
    if len(position) == 2:
        size = kwargs.get('size', [1920, 1080])
        position = [position[0], position[1], position[0] + size[0], position[1] + size[1]]
    delay = kwargs.get('delay', 1)
    folder = kwargs.get('folder', '')
    file_name = kwargs.get('file_name', 'screenshot.png')
    #take a screenshot
    print(f"Taking a screenshot at {position}...")
    pos = position
    screenshot = pyautogui.screenshot(region=(pos[0], pos[1], pos[2]-pos[0], pos[3]-pos[1]))
    #save the screenshot
    if folder != "":
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_name = f"{folder}\\{file_name}"
        print(f"Saving the screenshot to {file_name}...")
        screenshot.save(file_name)
    robo_delay(delay=delay)
    
def robo_pdf_from_svg(**kwargs):
    file_input = kwargs.get('file_input', '')
    file_output = kwargs.get('file_output', '')
    if file_output == '':
        file_output = file_input.replace('.svg', '.pdf')
    #convert using call to inkscape command line
    print(f"Converting {file_input} to {file_output}...")
    os.system(f"inkscape {file_input} --export-filename={file_output}")

def robo_pdf_merge(**kwargs):
    import PyPDF2
    folder = kwargs.get('folder', '')
    fil = kwargs.get('files', '')
    filters = kwargs.get('filters', ['.pdf'])
    file_output = kwargs.get('file_output', 'merged.pdf')
    #if filter is a string make it an array
    if isinstance(filters, str):
        filter = [filter]
    if fil == '':
        fil = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                #only include if all filters are in file
                file_full = os.path.join(root, file)
                if all(f in file_full for f in filters):
                    fil.append(file_full)

    
    
    #merge the pdf files
    print(f"Merging {len(fil)} pdf files into {file_output}...")
    merger = PyPDF2.PdfMerger()
    for pdf in fil:
        print(f"  adding {pdf}")
        merger.append(pdf)
    merger.write(file_output)
    merger.close()
