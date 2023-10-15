import os
import copy

def main(**kwargs):
    print("action_new_computer_setup.py main()")
    folder_path = []
    folder_path.append("c:/gh/oomlout_base")

    kwargs["folder_path"] = folder_path
    set_folder_path(**kwargs)

    folder_pythonpath = []
    folder_pythonpath.append("c:/gh/oomlout_base")
    
    kwargs["folder_pythonpath"] = folder_pythonpath
    set_folder_pythonpath(**kwargs)

    



def set_folder_path(**kwargs):
    environment_variable = "PATH"
    kwargs["environment_variable"] = environment_variable
    set_folder_generic(**kwargs)

def set_folder_pythonpath(**kwargs):
    environment_variable = "PYTHONPATH"
    kwargs = copy.deepcopy(kwargs)
    kwargs["folder_path"] = kwargs["folder_pythonpath"]    
    kwargs["environment_variable"] = environment_variable
    set_folder_generic(**kwargs)


def set_folder_generic(**kwargs):
    print("action_new_computer_setup.py set_folder_path()")
    folder_path = kwargs["folder_path"]
    environment_variable = kwargs.get("environment_variable", "PATH")
    for folder in folder_path:
        folder = folder.replace("/", "\\")
        print("folder: ", folder)
        #add folder to the path variable if it isn't already there using os.system it is windows
        path_current = os.environ['PATH']
        if not folder.lower() in path_current.lower():
            os.system(f'setx PATH "%PATH%;{folder}"')
            print("folder added to path: ", folder)
        else:
            print("folder already in path: ", folder)


if __name__ == '__main__':
    main()

