import shutil
import os
import yaml

def main(**kwargs):
    #get the project name    
    if True:
        #prompt for the name of the new project
        project_name = input("Project Name: ")
        directory_project = f'c:/gh/{project_name}'

    #create directory
    if True:
        #create the directory
        if not os.path.exists(directory_project):
              os.mkdir(directory_project)
    
    #copy the base project
    if True:
        directory_base_project = 'templates/oomp_project_base'
        file_skip = []
        #generated files
        file_skip.append("oolc_production/working.yaml")
        file_skip.append("working_manual.yaml")
        #implementing later
        file_skip.append("working_manual_teardown.yaml")
        file_skip.append("working_parts.ods")
        for file_name in os.listdir(directory_base_project):
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
        details = {}
        details["project_id"] = project_name
        details["project_name"] = f'{project_name.replace("_", " ").title()}'
        details["project_repo"] = f'https://github.com/oomlout/{project_name}'
        details["production_format"] = {}
        details["production_format"]["oolc_1"] = {}
        details["production_format"]["oolc_1"]["file_location"] = f'source_files/oolc_1.cdr'
        #dump the yaml        
        file_path = os.path.join(directory_project, "oolc_production/working.yaml")
        with open(file_path, 'w') as file:            
            yaml.dump(details, file, sort_keys=False)


    #run working.py to create the readme
    if False:
        #issue with the directory for the readme generation
        #import it as a module
        import sys
        sys.path.append(directory_project)
        import working
        working.main()

    #turn the directory into a git repo and register it with github
    if True:
        #use os system calls
        
        #set the directory for os system so it persists        
        os.system(f'cd {directory_project} && git init -b main')
        

        #add to gihub using github cli gh
        os.system(f'cd {directory_project} && gh repo create oomlout/{project_name} --public --confirm')
        pass

        #add origin to git
        git_repo = f"https://www.github.com/oomlout/{project_name}"
        os.system(f'cd {directory_project} && git remote add origin {git_repo}')        
        os.system(f'cd {directory_project} && git add .')
        os.system(f'cd {directory_project} && git commit -m "first commit"')
        os.system(f'cd {directory_project} && git branch -M main && git push -u origin main')



if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)