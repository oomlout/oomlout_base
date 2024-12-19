#a utility that iterates through the folder it was launched in and makes a list of all the files that adhere to a set of rules
#it then shows that list and prompts the user to delete the files if they wish

import os
import argparse


def list_files(directory, rules, **kwargs):
    prompt = kwargs.get('prompt', True)
    """
    List all files in the given directory that adhere to the specified rules.
    """
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if all(rule(file) for rule in rules):
                matching_files.append(os.path.join(root, file))
    return matching_files

def prompt_delete_files(files, **kwargs):
    """
    Prompt the user to delete the specified files.
    """
    for file in files:
        print(f"Found file: {file}")
    
    prompt = kwargs.get('prompt', True)
    if not prompt:
        confirm = 'y'
    else:
        confirm = input(f"Delete {len(files)} files? (y/n): ")
    if confirm.lower() == 'y':
        for file in files:
            os.remove(file)
            print(f"Deleted file: {file}")

def main(**kwargs):
    

    """
    Main function to list and optionally delete files based on rules.
    """
    directory = os.getcwd()
    rules = [
        lambda file: "_140.png" in file,
        lambda file: "_300.png" in file,
        lambda file: "_600.png" in file,
        lambda file: "_1000.png" in file,
        lambda file: "_140.jpg" in file,
        lambda file: "_300.jpg" in file,
        lambda file: "_600.jpg" in file,
        lambda file: "_1000.jpg" in file,

        #working.dxf
        lambda file: "working.dxf" in file,
        lambda file: "working.pdf" in file
    ]
    matching_files = []
    for rule in rules:
        matching_files.extend(list_files(directory, [rule], **kwargs))    
    #if working.png in base directory delete that
    if os.path.exists("working.png"):
        os.remove("working.png")
        print(f"Deleted file: working.png")
    prompt_delete_files(matching_files, **kwargs)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean up files based on rules.')   
    #-n -nop-prompt make it default to False 
    parser.add_argument('-n', '--no-prompt', action='store_true', help='Do not prompt for deletion.')
    
    args = parser.parse_args()
    
    print("args:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")

    kwargs = {}
    if args.no_prompt:
        kwargs['prompt'] = False
    
    # Call the main function with the parsed arguments
    print("kwargs:")
    for arg in kwargs:
        print(f"  {arg}: {kwargs[arg]}")
    main(**kwargs)
    