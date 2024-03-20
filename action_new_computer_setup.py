import os
import copy


def main(**kwargs):
    print("action_new_computer_setup.py main()")
    
    pip = True
    path = True
    pythonpath = True
    openscadpath = True
    clone = True
    install = True

    pip = False
    #path = False
    pythonpath = False
    openscadpath = False
    clone = False
    #install = False

    #run python_pip.bat
    if pip:
        os.system("action_python_pip.bat")
        

    # environment_variable = "PATH"
    if path:
        print("path()")
        folder_path = []
        folder_path.append("c:/gh/oomlout_base")
        # the_allotment
        folder_path.append("c:/gh/the_allotment")
        # ghost script
        folder_path.append("C:/Program Files/gs/gs9.54.0/bin") 
        #db path
        folder_path.append("c:/od/OneDrive/path") 
        #opsc
        folder_path.append("c:/gh/oomlout_opsc_version_3")
        #openscad
        folder_path.append("C:/Program Files/OpenSCAD")
        #corel
        folder_path.append("C:/Program Files/Corel/CorelDRAW Graphics Suite 2020/Programs64")   
        #inkscape
        folder_path.append("C:/Program Files/Inkscape/bin")
        # python
        folder_path.append("C:/Users/aaron/AppData/Local/Programs/Python/Python312")
        #oolc
        folder_path.append("C:/GH/oomlout_oolc_oopen_laser_cutting_production_format")
        

        kwargs["folder_path"] = folder_path
        set_folder_path(**kwargs)

    # environment_variable = "PYTHONPATH"
    if pythonpath:
        print("pythonpath()")   
        folder_pythonpath = []
        folder_pythonpath.append("c:/gh/oomlout_base")
        #opsc
        folder_pythonpath.append("c:/gh/oomlout_opsc_version_3")
        # oomp_src
        folder_pythonpath.append("C:/gh/oomlout_oomp_part_generation_version_1")
        # oolc
        folder_pythonpath.append("C:/gh/oomlout_oolc_oopen_laser_cutting_production_format")

        kwargs["folder_pythonpath"] = folder_pythonpath
        set_folder_pythonpath(**kwargs)

    if openscadpath:
        print("openscadpath()")   
        folder_openscadpath = []
        #opsc
        folder_openscadpath.append("c:/gh/oomlout_opsc_version_3")
        kwargs["folder_openscadpath"] = folder_openscadpath
        set_folder_openscadpath(**kwargs)

    # clone repos
    if clone:
        file_oomlout_repos = "oomlout_github_repos.yaml"

        kwargs["file_oomlout_repos"] = file_oomlout_repos
        clone_repos(**kwargs)

    if install:
        print(f"installing files")
        install_programs(**kwargs)

def clone_repos(**kwargs):
    file_oomlolout_repos = kwargs["file_oomlout_repos"]

    #load the repos
    import yaml
    with open(file_oomlolout_repos) as file:
        oomlout_repos = yaml.load(file, Loader=yaml.FullLoader)
    #loop through the repos
    for repo_id in oomlout_repos:
        repo = oomlout_repos[repo_id]        
        name = repo["name"]
        directory = repo.get("directory", "gh")
        directory = os.path.join("c:/", directory)
        url = repo.get("url", f"http://github.com/oomlout/{name}.git")
        import oom_git
        oom_git.clone(repo=url, directory=directory)


def install_programs(**kwargs):
    folder_base = "C:/od/OneDrive/install_files/install_files_new_computer"
    programs = []
    import glob
    #get all .exe from folder_base
    files = glob.glob(f"{folder_base}/*.exe")
    #add all .msi files
    files += glob.glob(f"{folder_base}/*.msi")
    for file in files:
        programs.append(file)


    for program in programs:
        choice = input(f"install {program}? (y/n)")
        if choice == "y":
            os.system(program)
        else:
            print(f"skipping {program}")

    


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

def set_folder_openscadpath(**kwargs):
    environment_variable = "OPENSCADPATH"
    kwargs = copy.deepcopy(kwargs)
    kwargs["folder_path"] = kwargs["folder_openscadpath"]    
    kwargs["environment_variable"] = environment_variable
    set_folder_generic(**kwargs)


def set_folder_generic(**kwargs):
    print("action_new_computer_setup.py set_folder_path()")
    folder_path = kwargs["folder_path"]
    environment_variable = kwargs.get("environment_variable", "PATH")    
    #print("folder: ", folder)
    #add folder to the path variable if it isn't already there using os.system it is windows

    path_current = os.environ.get(environment_variable, None)
    if path_current is None:
        os.environ[environment_variable] = ""
        path_current = os.environ[environment_variable]

    new_path = f'{path_current}'
    #split new path with ; and remove duplicates            
    new_path = new_path.split(";")
    new_path = list(set(new_path))
    #remove "" entries
    new_path = [x for x in new_path if x != ""]            
    for folder in folder_path:
        folder = folder.replace("/", "\\")
        # if fiolder not in any of new_path.lower()
        if not any(folder.lower() in s.lower() for s in new_path):
            new_path.append(folder)

    new_path = ";".join(new_path)
    new_path = new_path.replace("/", "\\")
    command = f'setx {environment_variable} "{new_path}"'
    os.system(command)
    # echo path using os.system
    #os.system(f'echo %PATH%')


    #print out the current path variable
    #path_current = os.environ['PATH']
    #print("path_current: ", path_current)


if __name__ == '__main__':
    main()

