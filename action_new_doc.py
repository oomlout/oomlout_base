import os 
import time
import pyautogui

def main(**kwargs):
    pass

    #get the doc name
    doc_name = kwargs['doc_name']
    doc_name_undercore = doc_name.replace(" ", "_") 
    doc_folder = f"C:\\od\\OneDrive\\docs\\{doc_name_undercore}"

    #if doc_fodler doesn't exist make it
    if not os.path.exists(doc_folder):
        os.makedirs(doc_folder)

    url_docs_template_file = "https://docs.google.com/document/d/10fXsYewkfDcijDNssGIfAJ6KB0AU2XdSdQq7oFXy0vE/edit?tab=t.0"

    #make a new doc
    #open the template
    if True:
        print(f"Opening the template file: {url_docs_template_file}")
        os.system(f"start {url_docs_template_file}")    
        #wait 10 seconds
        print("Waiting 10 seconds for the template to load")
        time.sleep(10)

    #copy the template
    if True:
        print("Copying the template")
        #press alt f
        pyautogui.hotkey('alt', 'f')
        time.sleep(1)
        
        #send c
        pyautogui.press('c')
        time.sleep(2)

        #send doc name
        pyautogui.typewrite(doc_name)
        time.sleep(2)

        #send t  ab five times
        tab_times = 5
        for i in range(tab_times):
            pyautogui.press('tab')
            time.sleep(0.25)
        
        #send enter
        pyautogui.press('enter')
        time.sleep(5)
        
        pyautogui.typewrite(doc_name)

        #press down 4 times
        down_times = 4
        for i in range(down_times):
            pyautogui.press('down')
            time.sleep(0.25)
        

        #send doc_folder
        pyautogui.typewrite(doc_folder)
                         

    #start doc fodler
    if True:
        os.system(f"start {doc_folder}")
    #close the template
    #rename the template



if __name__ == "__main__":
    import sys
    import argparse

    #parser = argparse.ArgumentParser(description="Process some kwargs.")
    #parser.add_argument('--kwargs', nargs='*', help="Key-value pairs", default=[])

    #args = parser.parse_args()
    #kwargs = dict(arg.split('=') for arg in args.kwargs)
    
    input = input("new doc name (spaces)")

    kwargs  ={}
    kwargs['doc_name'] = input

    main(**kwargs)