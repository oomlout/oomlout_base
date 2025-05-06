#import oom_kicad
#import oom_markdown
import os
#import copy
#import scad
import time
import pyautogui
import clipboard
import random

import robo

#process
#  locations set in working_parts.ods 
#  export to working_parts.csv
#  put components on the right side of the board
#  run this script

def get_all_directories(folder):
    #get a list of all the directories recursively in folder
    directories = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for dirname in dirnames:
            directories.append(os.path.join(dirpath, dirname))
    return directories

def main(**kwargs):
    folder = kwargs.get('folder', '')
    folders = get_all_directories(folder)
    #get a list of all the directories recursively in folder
    #print(f"folder: {folder}")
    #print(f"folder: {os.path.abspath(folder)}")
    pass
    #make_readme(**kwargs)

    for folder in folders:
        print(f"making resolution for: {folder}")
        working_file = os.path.join(folder, "working.png")
        if not os.path.exists(working_file):
            working_file = os.path.join(folder, "working.jpg")
            if not os.path.exists(working_file):
                working_file = os.path.join(folder, "working.jpeg")
        
        if os.path.exists(working_file):
            url_chat = "https://chatgpt.com/c"
            processed = True
            while processed:        
                if processed:
                    robo.robo_chrome_open_url(url=url_chat, delay=10)
                kwargs["working_file"] = working_file
                processed = get_upscale(**kwargs)
                if processed: 
                    robo.robo_keyboard_close_tab()
                    robo.robo_keyboard_press_escape()


def get_upscale(**kwargs):
    processed = False
    #setup
    
    working_file = kwargs.get('working_file', '')
    if os.path.exists(working_file):
        working_file_directory = os.path.dirname(working_file)
        working_file_just_file = os.path.basename(working_file)
        working_file_just_file_output = working_file_just_file.replace("working", "working_large")
        working_file_output = os.path.join(working_file_directory, working_file_just_file_output)
        working_file_output_absolute = os.path.abspath(working_file_output)
        working_file_input_absolute = os.path.abspath(working_file)

        test = True

        if test:            
            position_text_box = [420,3320]
            position_generated_image = [560,740]
            position_clip_prime = [885,618]
            position_add_file = [418,3318]  #big screen
            position_save_image = [461,3351]  #big screen
        else:
            position_text_box = [422,500]
            position_generated_image = [560,740]
            position_clip_prime = [885,618]
            position_add_file = [418,3318]  #big screen
            position_save_image = [461,3450]  #big screen

        #only if the file does not exist
        if not os.path.exists(working_file_output_absolute):
            print(f"creating")
            processed = True
        else:
            print(f"already exists skipping")
            return processed
        
        #upload source file
        if True:
            pass
            print(f"adding file {working_file_input_absolute}...")
            robo.robo_mouse_click(position=position_add_file)
            robo.robo_keyboard_press_down(repeat=3)
            robo.robo_keyboard_press_enter(delay=5)
            string = working_file_input_absolute
            robo.robo_keyboard_press_string(string=string)
            robo.robo_keyboard_press_enter(delay=20)

        
        #type prompt
        if True:
            #print(f"Clicking in the text box at {position_text_box}...")
            position = position_text_box
            prompt = f"""hiya chadiekins can i get you to upscale this image 2x but use an ai model rather than python?"""        
            robo.robo_chatgpt_prompt_type(prompt=prompt, position=position)
        

        
        #waiting for generation
        if True:
            strings_error = []
            strings_error.append("i hit a temporary limit")
            #strings_error.append("made with the old version")
            strings_error.append("unavailable")
            strings_error.append("technical issue")
            strings_error.append("rate limit")

            strings_waiting = []
            strings_waiting.append("getting started")
            strings_waiting.append("analyzing")
            strings_waiting.append("creating image")
            strings_waiting.append("adding detail")

            print("Waiting for the image to generate...")
            while True:
                #click on the clip prime spot
                clip = robo.robo_keyboard_copy(position=position_clip_prime)
                
                clip_last_500 = clip[-500:]
                if any(string in clip.lower() for string in strings_waiting):
                    print("Image not ready yet")
                    robo.robo_delay(delay=120)
                #check if any string_errors are in the clip
                elif  any(string in clip_last_500.lower() for string in strings_error): 
                    #wait here until i click okay
                    print("Image not ready yet, waiting for user to click okay...")
                    #wait using input
                    #input("Press enter to continue...")
                    base = 3600
                    extra = random.randint(0, base)
                    robo.robo_delay(delay=base,rand=extra)
                    prompt = "try again?"
                    robo.robo_chatgpt_prompt_type(prompt=prompt)
                else:
                    print("Image ready!")
                    break

        #save image
        if True:
            # diownload from python
            if False:
                directory_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
                #get list of files in a variable
                files_before = os.listdir(directory_downloads)
                #use a right click to click on the image wait for menu then down twice then enter
                print(f"Right clicking on the image at {position_generated_image}...")
                position = position_save_image
                robo.robo_mouse_click(position=position, button='left', delay=10)
                files_after = os.listdir(directory_downloads)
                #get the new file that was added to the downloads folder
                new_files = list(set(files_after) - set(files_before))
                #copy the new file to the working directory
                if len(new_files) > 0:
                    new_file = new_files[0]
                    new_file_path = os.path.join(directory_downloads, new_file)
                    print(f"new file: {new_file_path}")
                    #move the file to the working directory
                    os.rename(new_file_path, working_file_output_absolute)
                    print(f"moved {new_file_path} to {working_file_output_absolute}")
                else:
                    print("no new files found")
                    processed = False
            #ai model
            if True: 
                   

            

        #check for image existing
        if True:
            if os.path.exists(working_file_output_absolute):
                print(f"Image {working_file_output_absolute} saved successfully!")
            else:
                print(f"Image {working_file_output_absolute} not saved!")
                processed = False
                #input("Press enter to continue...")    
            
        #delay 30 with 120 rand
        if True:
            base = 120
            extra = 300
            robo.robo_delay(delay=base,rand=extra)
        
        return processed

def make_readme(**kwargs):
    os.system("generate_resolution.bat")
    oom_markdown.generate_readme_project(**kwargs)
    #oom_markdown.generate_readme_teardown(**kwargs)



    
if __name__ == '__main__':
    kwargs = {}
    #folder is the folder it was launched from not the location of the file
    folder_launch = os.getcwd()

    #test
    folder_launch = r"C:\od\OneDrive\docs\business_vintage_clothing_base\source_files\identity"

    print(f"folder: {folder_launch}")
    kwargs['folder'] = folder_launch


    main(**kwargs)