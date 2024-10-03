import os
import time


def main(**kwargs):
    print("household_kitchen_grocery_ocado_weekly_list_add_and_checkout")
    print("     ********************************************")
    print("     *** This script adds the weekly shopping list to the trolley and checks out ***")
    print("     ********************************************")
    
    #open the calendar page
    url_calendar = "https://www.ocado.com/webshop/getAddressesForDelivery.do"
    oom_open_url(url_calendar, message = "opening calendar page")

    input("          press enter after you have booked the delivery slot")
    #open the shopping list page
    url_shopping_list = "https://www.ocado.com/webshop/shoppingLists/display.go"
    oom_open_url(url_shopping_list, message = "opening shopping list page")
    
    #add list to trolley
    coordinate_add__list_to_trolley = (980,480)
    oom_click(*coordinate_add__list_to_trolley, time_delay = 5)
    
    # do the checkoout
    oom_household_kitchen_grocery_ocado_checkout()
    
    # print done
    print("done")

def oom_household_kitchen_grocery_ocado_checkout():
    import pyautogui

    #get display width
    screen_width = pyautogui.size().width
    screen_height = pyautogui.size().height
    print("Screen Width:", screen_width)
    #click checkout button

    coordinates_checkout = [(screen_width-50,170)]
    for coordinate_checkout in coordinates_checkout:
        oom_click(*coordinate_checkout, time_delay = 3, message = "clicking checkout button")
    #click continue button 5 times
    times = 5
    for i in range(times):     
        print(f"clicking continue button {i+1} times of {times}")   
        coordinate_continue = (screen_width-50,screen_height - 60)
        oom_click(*coordinate_continue, time_delay = 3)



def oom_delay(seconds):
    #if more than 3 seconds print a dot each second
    if seconds > 3:
        print(f"{seconds} seconds delay  ", end="")
        for i in range(seconds):
            print(".", end="")
            time.sleep(1)
        print()
    else:   
        time.sleep(seconds)

def oom_click(x, y, time_delay=0.5, message = ""):
    #import pyautogui
    import pyautogui
    #print message
    if message != "":
        print(message)
    #move mouse to x, y
    pyautogui.moveTo(x, y)
    #click left mouse button
    pyautogui.click()
    #wait for the time delay
    oom_delay(time_delay)

def oom_open_url(url, time_delay=5, message = ""):
    #import os
    import os
    #open the url
    os.system(f"start {url}")
    #wait for the time delay
    if message == "":
        message = f"opening {url}"
    print(message)
    oom_delay(time_delay)

if __name__ == "__main__":
    main()