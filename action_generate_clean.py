#a utility that iterates through the folder it was launched in and makes a list of all the files that adhere to a set of rules
#it then shows that list and prompts the user to delete the files if they wish

import os

def list_files(directory, rules):
    """
    List all files in the given directory that adhere to the specified rules.
    """
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if all(rule(file) for rule in rules):
                matching_files.append(os.path.join(root, file))
    return matching_files

def prompt_delete_files(files):
    """
    Prompt the user to delete the specified files.
    """
    for file in files:
        print(f"Found file: {file}")
    confirm = input("Do you want to delete these files? (y/n): ")
    if confirm.lower() == 'y':
        for file in files:
            os.remove(file)
            print(f"Deleted file: {file}")

def main():
    """
    Main function to list and optionally delete files based on rules.
    """
    directory = os.getcwd()
    rules = [
        #has _140. in it
        lambda file: "_140.png" in file,
        #has _300. in it
        lambda file: "_300.png" in file,
        #has _600. in it
        lambda file: "_600.png" in file,
        #has _1000. in it
        lambda file: "_1000.png" in file,
        #working.dxf
        lambda file: "working.dxf" in file,
        lambda file: "working.pdf" in file
    ]
    matching_files = []
    for rule in rules:
        matching_files.extend(list_files(directory, [rule]))    
    #if working.png in base directory delete that
    if os.path.exists("working.png"):
        os.remove("working.png")
        print(f"Deleted file: working.png")
    prompt_delete_files(matching_files)
    

if __name__ == '__main__':
    main()