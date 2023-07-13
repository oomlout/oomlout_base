import imageio
import os
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from pathlib import Path
import shutil
import win32api
import win32con
import pyperclip
import time


# json functions
def json_dump(obj, file_path):
    with open(file_path, 'w') as f:
        json.dump(obj, f)

def json_load(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

###### Batch file running
import subprocess

def batch_run(command):
  process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
  while True:
    line = process.stdout.readline()
    if line:
      print(line.decode().rstrip())
    else:
      break



# string functions
def string_between(input_string, start_string, end_string):
    start_index = input_string.find(start_string)
    if start_index == -1:
        return "" # start_string not found
    start_index += len(start_string)
    end_index = input_string.find(end_string, start_index)
    if end_index == -1:
        return "" # end_string not found
    return input_string[start_index:end_index]

import json
def string_dict_pretty(dicts):
    if not isinstance(dicts, list):
        dicts = [dicts]
    formatted_dicts = []
    for my_dict in dicts:
        formatted_dict = json.dumps(my_dict, indent=4)
        formatted_dicts.append(formatted_dict)
    return formatted_dicts

# print functions
def print_split(my_strings):
    if isinstance(my_strings, str):
        my_strings = [my_strings]
    for my_string in my_strings:
        lines = my_string.split("\n")
        for line in lines:
            print(line)

###### Clipboard
import time
import pyperclip
import win32api
import win32gui

import time
import pyperclip
import win32api

def clipboard_wait(wait, in_clipboard=True, point=None, poll_time=10, wait_limit=-1, remove_line_break=False):
    if isinstance(wait, str):
        wait = [wait]  # Convert the string to a single-element list
    print(f'Waiting for {"all" if in_clipboard else "none"} of {wait} to be in clipboard')
    iteration = 0
    while True:
        if point is not None:
            mouse_click(point,button="DOUBLE")

        pyperclip.copy("")  # Clear the clipboard

        # Press Ctrl+A and Ctrl+C to copy the contents of the clipboard
        keyboardPress("a", pause=1, alt="ctrl",debug=False)
        keyboardPress("c", pause=1, alt="ctrl",debug=False)

        # Read the contents of the clipboard
        clipboard_contents = pyperclip.paste()
        clipboard_contents = clipboard_contents.replace("\n","").replace("\r","")
        #print(clipboard_contents)

        # Check if all of the wait strings are (or are not) in the clipboard contents
        if all(w in clipboard_contents for w in wait) == in_clipboard:
            # Check if none of the wait strings are (or are not) in the clipboard contents
            if all(w not in clipboard_contents for w in wait) != in_clipboard:
                print(" done")  # Print a newline
                return True

        # Print a dot and increment the iteration counter
        print('.', end='', flush=True)
        iteration += 1

        # Check if the wait limit has been reached
        if wait_limit > 0 and iteration >= wait_limit:
            print(" wait limit exceeded")  # Print a newline
            return False

        # Sleep for the specified poll time before checking again
        time.sleep(poll_time)



###### DIRECTORIES

def dir_num_files(dir_path):
    """
    Returns the number of files in the specified directory.
    """
    import os

    # Get a list of all the files in the directory
    file_list = os.listdir(dir_path)

    # Return the length of the list (i.e., the number of files)
    return len(file_list)

###### folder manipulation

def folder_copy_filtered(input_dir, output_dir, filter_string):
    print("Copying folders from: " + input_dir + " to: " + output_dir)
    for dirpath, dirnames, filenames in os.walk(input_dir):
        for dirname in dirnames:
            if filter_string in dirname:
                src = os.path.join(dirpath, dirname)
                dst = os.path.join(output_dir, dirname)
                ping(1)
                shutil.copytree(src, dst)

def folder_move_filtered(input_dir, output_dir, filter_string):
    print("Moving folders from: " + input_dir + " to: " + output_dir)
    for dirpath, dirnames, filenames in os.walk(input_dir):
        for dirname in dirnames:
            if filter_string in dirname:
                src = os.path.join(dirpath, dirname)
                dst = os.path.join(output_dir, dirname)
                print("    Moving: " + src + " to: " + dst)
                shutil.move(src, dst)
    return dst

def folder_delete_contents(root_folder):
    print("Deleting contents of folder: " + root_folder)
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for dirname in dirnames:
            folder_path = os.path.join(dirpath, dirname)
            print("    Deleting: " + folder_path)
            shutil.rmtree(folder_path)   

# array functions

def array_sort(data, sort_key, reverse=False):
    def sort_by_numeric_value(d):
        try:
            return int(d[sort_key])
        except ValueError:
            return d[sort_key]
    try:
        print("data sorted")
        sorted_data = sorted(data, key=sort_by_numeric_value)
        return sorted_data
    except:
        print("slight sorting error but okay")
        sorted_data = sorted(data, key=lambda d: d[sort_key])
        return sorted_data

def array_filter(data, filter_strs, all_filters=True):
    filtered_data = []
    if isinstance(filter_strs,str):
        filter_strs = [filter_strs]
    for item in data:
        matched = False
        if isinstance(item, str):
            for filter_str in filter_strs:
                if filter_str in item:
                    matched = True
                    if not all_filters:
                        break
                elif all_filters:
                    matched = False
                    break
        elif isinstance(item, list) or isinstance(item, dict):
            for filter_str in filter_strs:
                if filter_str in str(item):
                    matched = True
                    if not all_filters:
                        break
                elif all_filters:
                    matched = False
                    break
        if matched:
            filtered_data.append(item)

    return filtered_data

###### file functions


def file_get_name_from_path(file_path):
    return os.path.basename(file_path)

####CHATGPT
####Can you show me a python routine that takes in a directory and returns a list of the directories in that directory in string format please
####
def getDirectoriesIn(directory):
    # Get a list of all files and directories in the specified directory
    dir_list = os.listdir(directory)

    # Filter out any non-directory items in the list
    dirs = [item for item in dir_list if os.path.isdir(os.path.join(directory, item))]

    # Return the list of directories as strings
    return [str(d) for d in dirs]

###can you show me the code to allow it to take in a directory called input_dir, and return an array of all the files with the extension filetype, I'd also likeit to have a boolean defaulted to false as to whether it should recursively look in the folders to get all files of the supplied type, and another boolean called full_path which defaults to False, if true it includes the full pathname for the file, if false the relative one

#### move files to laser directory
##### Can I get a python function that take in an input directory, output directory and a file type, and extra bit, it then copies all the files in the input directory to the output directory adding the extra bit to their filename
##### please make it overwrite the file if it already exists
##### and add an underscore before the extrabit is added


def files_copy_laser(input_directory, index):
    print("Copying files to laser directory: " + input_directory)
    input_directory = input_directory
    output_directory = "C:\\DB\\Dropbox\\LALA-Laser Files"
    file_type = ".dxf"
    extra_bit = str(index).zfill(2)
    files_copy_with_extra_bit(input_directory, output_directory, file_type, extra_bit)

def files_copy_with_extra_bit(input_directory, output_directory, file_type, extra_bit):
    # Make sure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Walk through the input directory and copy each file that matches the file type
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(file_type):
                # Use the "copyfile" function instead of "copy2" to overwrite the file if it already exists in the output directory
                shutil.copyfile(os.path.join(root, file), os.path.join(output_directory, file))
                # Rename the file by adding an underscore and the extra bit to the end of the filename before the file extension
                renamed_file = file[:-len(file_type)] + "_" + extra_bit + file_type
                # Overwrite the renamed file if it already exists in the output directory
                os.replace(os.path.join(output_directory, file), os.path.join(output_directory, renamed_file))

def fileGetNameList(input_dir, filetype, path_type="relative"):
    # Create an empty list to store the filenames
    filenames = []

    # Check if the input directory exists
    if not os.path.exists(input_dir):
        return filenames

    # Loop through all files and directories in the input directory
    for entry in os.listdir(input_dir):
        # Construct the full path of the entry
        entry_path = os.path.join(input_dir, entry)

        # Check if the entry is a file
        if os.path.isfile(entry_path):
            # Check if the file is of the specified file type
            if entry.endswith(filetype):
                # Add the filename to the list
                if path_type == "relative":
                    filenames.append(entry)
                elif path_type == "full":
                    filenames.append(entry_path)
                elif path_type == "both":
                    filenames.append((entry, entry_path))
                    
    # Return the list of filenames
    return filenames

import shutil
import time
import os

# Global variable to store the start time
start_time = 0

import shutil


def file_copy_filter(input_dir, output_dir, filter_str, check_all=True, recursive=True, debug=True):
    # If filter_str is a string, convert it to a list
    if isinstance(filter_str, str):
        filter_str = [filter_str]

    # Walk through the input directory recursively if recursive=True
    if recursive:
        walk_generator = os.walk(input_dir)
    else:
        walk_generator = [(input_dir, [], [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))])]

    # Iterate over files in the input directory and its subdirectories
    for root, _, files in walk_generator:
        for file in files:
            # Check if the file matches the filter
            match_count = 0
            for filter_item in filter_str:
                if filter_item in file:
                    match_count += 1
                    if not check_all:
                        break
            if (check_all and match_count == len(filter_str)) or (not check_all and match_count > 0):
                # If the file matches the filter, copy it to the output directory
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_dir, file)
                if not os.path.exists(output_path):
                    os.makedirs(output_dir, exist_ok=True)
                shutil.copyfile(input_path, output_path)
                if debug:
                    print(f"Copied file {input_path} to {output_path}")

    if debug:
        print("Finished copying files.")

def file_move_filter(input_dir, output_dir, filter_str, check_all=True, recursive=True, debug=True):
    # If filter_str is a string, convert it to a list
    if isinstance(filter_str, str):
        filter_str = [filter_str]

    # Walk through the input directory recursively if recursive=True
    if recursive:
        walk_generator = os.walk(input_dir)
    else:
        walk_generator = [(input_dir, [], [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))])]

    # Iterate over files in the input directory and its subdirectories
    for root, _, files in walk_generator:
        for file in files:
            # Check if the file matches the filter
            match_count = 0
            for filter_item in filter_str:
                if filter_item in file:
                    match_count += 1
                    if not check_all:
                        break
            if (check_all and match_count == len(filter_str)) or (not check_all and match_count > 0):
                # If the file matches the filter, copy it to the output directory
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_dir, file)
                if not os.path.exists(output_path):
                    os.makedirs(output_dir, exist_ok=True)
                shutil.move(input_path, output_path)
                if debug:
                    print(f"Copied file {input_path} to {output_path}")

    if debug:
        print("Finished copying files.")


def file_copy_recent(src="", dst="", move=False, reset=False, debug=False):
    global start_time
    
    # Reset the start time if requested
    if reset:
        start_time = time.time()
        return True
    
        
    
    # Print a table of all the files being analyzed if debug is True
    if debug:
        print('File Name                                              | Creation Time             | Action')
        print('-------------------------------------------------------------------------------------------')
    
    # Iterate through all files in the src directory
    for file in os.listdir(src):
        # Create the dst directory if it doesn't already exist and dst is not an empty string
        if dst:
            os.makedirs(dst, exist_ok=True)
        
        file_path = os.path.join(src, file)
        # Print the file name and creation time
        if debug:
            print(f'{file:50} | {time.ctime(os.path.getctime(file_path)):25} | ', end='')
        # Check if the file was created since the start time
        if os.path.getctime(file_path) >= start_time:
            # Print the action (copy or move)
            if debug:
                print(f'{("Move" if move else "Copy"):6}')
            # Construct the destination file path
            dst_file = os.path.join(dst, file)
            # Move or copy the file to the destination directory
            if move:
                shutil.move(file_path, dst_file)
            else:
                shutil.copy(file_path, dst_file)
        elif debug:
            print()

import hashlib

def file_get_hash(filename):
    # Initialize the hash object
    sha256 = hashlib.sha256()
    try:
        # Open the file in binary mode and read it in chunks
        with open(filename, "rb") as f:
            while True:
                # Read in a chunk of data
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                # Update the hash object with the chunk
                sha256.update(chunk)
        # Return the hexadecimal representation of the hash
    except Exception as e:
        print(f'hash error {filename}')
        print(e)
        return ""
    return sha256.hexdigest()


def file_find_replace(filename, string_pairs):
    with open(filename, 'r') as file:
        data = file.read()

    for pair in string_pairs:
        old_str, new_str = pair
        data = data.replace(old_str, new_str)

    with open(filename, 'w') as file:
        file.write(data)

def file_get_largest_file_in_dir(dir_path, recursive=True):
    """
    Finds the path to the largest file in the given directory.

    Args:
    dir_path (str): The path to the directory to search in.
    recursive (bool): Whether to search recursively or not. Default is True.

    Returns:
    str: The full path to the largest file found.
    """
    largest_file_path = ""
    largest_file_size = 0
    
    if recursive:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) > largest_file_size:
                    largest_file_path = file_path
                    largest_file_size = os.path.getsize(file_path)
    else:
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path) and os.path.getsize(file_path) > largest_file_size:
                largest_file_path = file_path
                largest_file_size = os.path.getsize(file_path)

    return largest_file_path

###can you show me a python function tcalled makedir that takes in a pathname called input_dir, checks if the directory already exists if it doesn't makes all required directories and prints a debug message if the directory is made telling the user the name of the directory being made or if the directory already exists tells them this please.
def dirMake(input_dir):
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print("Directory '%s' created" % input_dir)
    else:
        print("Directory '%s' already exists" % input_dir)
###can you show me a python fnction called fileCopy that takes in a file name called file_in and copies it to a file defined by an input called file_out, can you check to make sure the directories for file_out exist and if they don't create them, also please include a print command that tells the user if the file is created, if the file already exists please tell them it already exists and is being overwritten, please include an input boolean called overwrite that when True overwrites the file and when false skips writing the file, please tell the user what happens regardless of the outcome 
def file_copy(file_in, file_out, overwrite=True):
    fileCopy(file_in, file_out, overwrite)
        
def fileCopy(file_in, file_out, overwrite=True):
    dirMake(os.path.dirname(file_out)) # Make sure the directories for file_out exist
    if not os.path.exists(file_out) or overwrite:
        shutil.copyfile(file_in, file_out)
        if not os.path.exists(file_out):
            print("File '%s' created" % file_out)
        else:
            print("File '%s' overwritten" % file_out)
    else:
        print("File '%s' already exists and will not be overwritten" % file_out)

import os
import glob
import shutil

def file_copy_wild(file_name, output_file, delete_source=False):
  """
  Copies the most recently modified file in the current directory that
  matches the given file name pattern to the specified output file. The
  file name pattern can include the '*' wildcard to match any string at
  that position. If delete_source is True, the source file will be
  deleted after being copied. If the output file already exists, it will
  be overwritten.
  """
  # Find all files in the current directory that match the file_name
  # pattern, using glob.glob
  matching_files = glob.glob(file_name)
  if len(matching_files) > 0:
    # If at least one matching file was found, sort the list of matching
    # files by modification time, with the most recently modified file
    # first
    matching_files.sort(key=os.path.getmtime, reverse=True)
    # Print a message indicating the file that is being copied and the
    # destination file
    print(f"Copying file {matching_files[0]} to {output_file}")
    # Create the directory structure for the output file, if it doesn't
    # already exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    # Copy the file to the output file
    shutil.copy(matching_files[0], output_file)
    # If delete_source is True, delete the source file
    if delete_source:
      os.remove(matching_files[0])
  else:
    # If no matching file was found, print an error message
    print(f"Error: no file found matching pattern {file_name}")


def file_copy_search(input_dir, search_strings, flat=False, copy_files=True, output_dir=None):
    """
    Search for files in input_dir containing all search_strings. Copy files to output_dir
    if copy_files is True. If recursive is True, search subdirectories recursively.
    Return a list of found files if copy_files is False.
    """
    found_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if all(s in file for s in search_strings):
                file_path = os.path.join(root, file)
                found_files.append(file_path)
                if copy_files:
                    if output_dir is None:
                        output_dir = input_dir
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    if flat:
                        shutil.copy(file_path, output_dir)
                    else:
                        rel_path = os.path.relpath(file_path, input_dir)
                        output_path = os.path.join(output_dir, rel_path)
                        output_dir_path = os.path.dirname(output_path)
                        if not os.path.exists(output_dir_path):
                            os.makedirs(output_dir_path)
                        shutil.copy(file_path, output_path)
    if copy_files:
        print("Copied files:")
        for file in found_files:
            print(os.path.basename(file))
    else:
        print("Found files:")
        for file in found_files:
            print(os.path.basename(file))
        return found_files

###Can you write me a python routine that takes a file_in variable and opens it returning a filehandle, please open the file in unicode format, also takein a mode variable this mode can be, read, write, append
def file_openpen(file_in, mode):
    return fileOpen(file_in, mode)

def fileOpen(file_in, mode):
        # Convert the mode argument to a character
    if isinstance(mode, str):
        if mode.lower() == "read":
            mode = "r"
        elif mode.lower() == "write":
            mode = "w"
        elif mode.lower() == "append":
            mode = "a"
        else:
            raise ValueError("Invalid mode")
    elif not isinstance(mode, str) and len(mode) != 1:
        raise ValueError("Invalid mode")

    # Open the file in the specified mode
    # Return the file handle
    return open(file_in, mode, encoding="utf-8")

import os

def file_write_line(file_name, line, debug=True, overwrite=False):
    if isinstance(lines, str):
        lines = [lines]
    if not overwrite or not os.path.exists(file_name):
        # Create any necessary directories
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        # Write lines to file
        with open(file_name, 'a', encoding='utf-8') as f:
            for line in lines:
                f.write(line + "\n")

        # Print debug statement
        if debug:
            print(f"writing {lines[0][:10]}... to {os.path.basename(file_name)}")
    else:    
        # truncate the file
        open(file_name, 'w').close()
        # write the new lines
        with open(file_name, 'a', encoding='utf-8') as f:
            for line in lines:
                f.write(line + "\n")
        if debug:
            print(f"Overwriting {os.path.basename(file_name)}")
    

###### IMAGES

###### given this python program
## can you make it take in a boolean overwrite if true it saves the cropped image if false it only creates the cropped image if the output filename doesn't exist
def imageCenterCropResize(input_dir, output_dir, output_resolution=512, overwrite=False):
    # Make the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):        
        
        # Check if the output file already exists
        output_path = os.path.join(output_dir, filename)
        if not os.path.exists(output_path) or overwrite:
            ping(1)
            # Open the image
            with Image.open(os.path.join(input_dir, filename)) as image:
                # Center crop the image to a 1:1 aspect ratio
                width, height = image.size
                cropped_dim = min(width, height)
                left = (width - cropped_dim) // 2
                top = (height - cropped_dim) // 2
                right = (width + cropped_dim) // 2
                bottom = (height + cropped_dim) // 2
                image = image.crop((left, top, right, bottom))

                # Resize the image to the specified output resolution
                image = image.resize((output_resolution, output_resolution), Image.LANCZOS)

                # Save the image
                image.save(output_path)
    ping("exit")

#Can you show me a python function that takes in a directory of images and expands them so the entire image is framed in a square and scale to a resol;ution that is a input variable
##can you make the same chances you did to the previous function only having it generate the crop if the filename doesn't already exist
### can you add a check and only convert if the file is an image please

def imageCenterExpandResize(input_dir, output_dir, resolution):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through all images in the input directory
    for filename in os.listdir(input_dir):
        
        # Check if the output file already exists
        output_path = os.path.join(output_dir, filename)
        if not os.path.exists(output_path):
            ping(1)
            # Open the image
            if ".jpg" in filename or ".png" in filename:
                with Image.open(os.path.join(input_dir, filename)) as img:
                    # Calculate the width and height of the image
                    width, height = img.size

                    # Calculate the size of the longest side of the image
                    max_size = max(width, height)

                    # Create a new image that is a square with the longest side as its length
                    new_img = Image.new('RGB', (max_size, max_size), color=(255, 255, 255))

                    # Calculate the offset for centering the original image within the new square image
                    offset = (int((max_size - width) / 2), int((max_size - height) / 2))

                    # Paste the original image into the new square image
                    new_img.paste(img, offset)

                    # Resize the new image to the specified resolution
                    new_img = new_img.resize((resolution, resolution), resample=Image.BILINEAR)

                    # Save the resized image to the output directory
                    new_img.save(output_path)
    ping("exit")

##### Keyboard
import pyautogui
import time

def keyboardPress(buttons=None, specialKey=None, times=1, pause=0.25, delay=0.03, alt='',debug=False):
    keyboard_press(buttons=buttons, special_key=specialKey, times=times, pause=pause, delay=delay, alt=alt,debug=debug)


#https://chat.openai.com/chat/9adc2900-4ff5-4e59-a22b-d6b8ef87f8bc
def keyboard_press(buttons=None, special_key=None, times=1, pause=0.25, delay=0.03, alt='',debug=False):
    if special_key:
        # Press the special key with optional modifiers
        if debug:
            print(f"Pressing {special_key} button {times} times")
        for i in range(times):
            # Print debug message
           
            pyautogui.keyDown(special_key)
            
            time.sleep(delay)
            pyautogui.keyUp(special_key)
    elif buttons:
        # Press the buttons with optional modifiers
        for i in range(times):
            # Print debug message
            if debug:
                print(f"Pressing {buttons} button(s)")
            if 'shift' in alt:
                pyautogui.keyDown('shift')
            if 'ctrl' in alt:
                pyautogui.keyDown('ctrl')
            if 'alt' in alt:
                pyautogui.keyDown('alt')
            for key in buttons:
                pyautogui.press(key)                
            if 'shift' in alt:
                pyautogui.keyUp('shift')
            if 'ctrl' in alt:
                pyautogui.keyUp('ctrl')
            if 'alt' in alt:
                pyautogui.keyUp('alt')
            # Wait for the specified pause
            time.sleep(pause)


##### MOUSE

def mouse_click(x, y=-1, button="LEFT", delay=0.25, debug=False):
  if isinstance(x, (list, tuple)):
    x, y = x
  # Convert button string to button constant
  if button == "LEFT":
    button = win32con.MOUSEEVENTF_LEFTDOWN
    release = win32con.MOUSEEVENTF_LEFTUP
  elif button == "RIGHT":
    button = win32con.MOUSEEVENTF_RIGHTDOWN
    release = win32con.MOUSEEVENTF_RIGHTUP
  elif button == "MIDDLE":
    button = win32con.MOUSEEVENTF_MIDDLEDOWN
    release = win32con.MOUSEEVENTF_MIDDLEUP
  # Print debug message
  if debug:
    print("Moving mouse to position ({}, {}) and clicking {} button".format(x, y, button))
  # Move the mouse to the specified position
  win32api.SetCursorPos((x, y))
  # Double-click the mouse if specified
  if button == "DOUBLE":
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
  # Click the mouse
  else:
    win32api.mouse_event(button, x, y, 0, 0)
    # Release the mouse button
    win32api.mouse_event(button, x, y, 0, release)
  # Wait for the specified delay
  time.sleep(delay)


#https://chat.openai.com/chat/b29e522b-b150-4395-bf8f-5b8c786b13e1
def mouse_scroll(scroll_amount: int, debug: bool = False):
    if debug:
        print(f"Scrolling mouse {scroll_amount} units")
    pyautogui.scroll(scroll_amount)



###### VIDEO
import imageio
import os

def create_animation(directory, out_file=None, debug=True):
    # Get all PNG or JPG files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.png') or f.endswith('.jpg')]

    # Sort the files based on their name
    files.sort()

    # Create an empty list to store the images
    images = []

    # Add each image to the list
    for file in files:
        images.append(imageio.imread(os.path.join(directory, file)))

    # Set the output file
    if not out_file:
        out_file = os.path.join(directory, "animation.mp4")
    if debug:
        print(f'Creating animation with {len(images)} images')
    # Create the animation
    imageio.mimsave(out_file, images)


def videoFromImages(input_dir, output_filename='output.avi', label=False):
    # Create an empty list to store the images
    images = []

    # Loop through all the files in the input directory
    for file_name in os.listdir(input_dir):
        ping(10)
        # Only include files with the supported image file extensions
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # Load the image
            file_path = os.path.join(input_dir, file_name)
            image = imageio.imread(file_path)

            # Convert the image from a numpy array to a PIL Image
            image = Image.fromarray(image)
            image = image.convert('RGB')
            # If the label parameter is True, add the filename to the image
            if label:
                # Create a new image with a white background and the same size as the original image
                image_with_text = Image.new('RGB', image.size, (255, 255, 255))

                # Draw the original image on the new image
                image_with_text.paste(image)

                # Load a font and draw the filename on the image
                font = ImageFont.truetype('arial.ttf', 14)
                ImageDraw.Draw(image_with_text).text((10, 10), file_name, font=font, fill=(255, 255, 255))

                # Add the new image with the filename to the list of images
                images.append(image_with_text)
            else:
                # If the label parameter is False, add the original image to the list of images
                images.append(image)

    # Save the images as an mp4 file
    output_path = os.path.join(input_dir, output_filename)
    imageio.mimwrite(output_path, images, format='mp4')


####### UTILITY
pinger = 0
def ping(divider=100):
    global pinger
    if divider == "exit":
        if pinger > 0:
            print()
        pinger=0
        
    else:
        pinger=pinger+1
        if pinger % divider == 0:
            print(".",end="")

import keyboard

def delay(delay=1,escape=True):
    t = delay
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