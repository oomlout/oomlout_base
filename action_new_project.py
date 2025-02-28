import shutil
import os
import yaml

def main(**kwargs):
    url_project_base_google_docs = "https://docs.google.com/document/d/1kq0wAvB6xJ0g4aAaEd-CLikVnkbmCYqg_ufLErMCwQo/edit"
    #open the google docs
    os.system(f'start {url_project_base_google_docs}')
    #open hardware spreadsheet
    url_oomp_open_hardware_spreadsheet = "https://docs.google.com/document/d/1w2YXTGAi3CJBH51rvx9MS1SsJaPUdVnEo-PXjtVu5WQ/edit?tab=t.0"
    os.system(f'start {url_oomp_open_hardware_spreadsheet}')


    #get the project name    
    project_type = input("Project Type (1: git, 2: local): ")
    if project_type == "":
        project_type = "git"
    if project_type == "1":
        project_type = "git"
    if project_type == "2":
        project_type = "local"
    
    if True:
        #prompt for the name of the new project
        project_name = input("Project Name: ")
        #clip to max 99 characters
        project_name = project_name[:99]
        if project_type == "git":
            directory_project = f'c:\\gh\\{project_name}'
        else:
            directory_project = f'c:\\od\\OneDrive\\docs\\{project_name}'

    #create directory
    if True:
        #create the directory
        if not os.path.exists(directory_project):
              os.mkdir(directory_project)
    
    #copy the base project
    if True:
        directory_base_project = 'templates\\oomp_project_base'
        file_skip = []
        #generated files
        file_skip.append("oolc_production\\working.yaml")
        file_skip.append("working_manual.yaml")
        #implementing later
        file_skip.append("working_manual_teardown.yaml")
        file_skip.append("working_parts.ods")
        #copy files and directories using recusrion
        import glob
        files = glob.glob(f'{directory_base_project}/**/*', recursive=True)
        for file_name in files:        
            file_name = file_name.replace("/", "\\")
            file_name = file_name.replace(f"{directory_base_project}\\", "")
            if file_name in file_skip:
                continue
            file_path = os.path.join(directory_base_project, file_name)
            file_path_new = os.path.join(directory_project, file_name)
            if os.path.isdir(file_path):
                if not os.path.exists(file_path_new):
                    os.mkdir(file_path_new)            
            else:
                shutil.copy(file_path, file_path_new)
            

    #create the working_manual.yaml
    if True:
        details = {}
        details["id"] = project_name
        details["name"] = f'{project_name.replace("_", " ").title()}'
        details["description"] = f'{project_name.replace("_", " ").title()}'
        details["readme_manual"] = ""
        #dump the yaml        
        file_path = os.path.join(directory_project, "working_manual.yaml")
        with open(file_path, 'w') as file:
            yaml.dump(details, file, sort_keys=False)

    #create the oolc_production/working.yaml
    if True:
        working_yaml_string = ""
        #details = {}
        working_yaml_string += "id: " + project_name + "\n"
        #details["project_id"] = project_name
        working_yaml_string += "project_name: " + f'{project_name.replace("_", " ").title()}' + "\n"
        #details["project_name"] = f'{project_name.replace("_", " ").title()}'
        working_yaml_string += "project_description: " + f'{project_name.replace("_", " ").title()}' + "\n"
        #details["project_repo"] = f'https://github.com/oomlout/{project_name}'
        working_yaml_string += f"project_repo: https://github.com/oomlout/{project_name}" + "\n"
        #details["production_format"] = 
        working_yaml_string += "#production_format: " + "\n"
        #details["production_format"]["oolc_1"] = 
        working_yaml_string += "#  oolc_1: " + "\n"        
        #details["production_format"]["oolc_1"]["file_location"] = f'source_files/oolc_1.cdr
        working_yaml_string += "#    file_location: " + f'source_files/oolc_1.cdr' + "\n"
        #dump the yaml        
        #file_path = os.path.join(directory_project, "oolc_production/working.yaml")
        #with open(file_path, 'w') as file:            
        #    yaml.dump(details, file, sort_keys=False)
        file_path = os.path.join(directory_project, "oolc_production/working.yaml")
        with open(file_path, 'w') as file:
            file.write(working_yaml_string)


    #run working.py to create the readme
    if False:
        #issue with the directory for the readme generation
        #import it as a module
        import sys
        sys.path.append(directory_project)
        import working
        working.main()

    #turn the directory into a git repo and register it with github
    if project_type == "git":
        #use os system calls
        
        #set the directory for os system so it persists        
        os.system(f'cd {directory_project} && git init -b main')
        

        #add to gihub using github cli gh
        command = f'cd {directory_project} && gh repo create oomlout/{project_name} --public --confirm'
        os.system(command)
        pass

        #add origin to git
        git_repo = f"https://www.github.com/oomlout/{project_name}"
        os.system(f'cd {directory_project} && git remote add origin {git_repo}')        
        os.system(f'cd {directory_project} && git add .')
        os.system(f'cd {directory_project} && git commit -m "first commit"')
        os.system(f'cd {directory_project} && git branch -M main && git push -u origin main')

    #open the folder in explorer
    if True:
        used_directory_project = directory_project.replace("/", "\\")
        os.system(f'explorer {used_directory_project}')
        # open in vscode
        os.system(f'code {used_directory_project}')

    #open working.cdr
    if True:
        file_path = f"{directory_project}\\working.cdr"
        os.system(f'start {file_path}')

if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)