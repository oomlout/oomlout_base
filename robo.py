import pyautogui
import clipboard
import random
import time
import os

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

#press string
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
        print(f"<<<<<>>>>> waiting for {delay} seconds")
    
        splits = 10
        for i in range(splits):
            #print the progress bar
            print(".", end='', flush=True)
            time.sleep(delay/splits)
        print("")
    else:
        print(f"waiting for {delay} seconds", end='', flush=True)
        for i in range(delay):
            #print the progress bar
            print(".", end='', flush=True)
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