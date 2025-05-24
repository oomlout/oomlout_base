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

def robo_keyboard_select_all(**kwargs):
    delay = kwargs.get('delay', 1)
    #select all
    print("selecting all")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
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