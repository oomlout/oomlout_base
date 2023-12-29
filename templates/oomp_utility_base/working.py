import os
import yaml
import glob

folder_configuration = "configuration"
folder_configuration = os.path.join(os.path.dirname(__file__), folder_configuration)
file_configuration = os.path.join(folder_configuration, "configuration.yaml")
#check if exists
if not os.path.exists(file_configuration):
    print(f"no configuration.yaml found in {folder_configuration} using default")
    file_configuration = os.path.join(folder_configuration, "configuration_default.yaml")



#import configuration
configuration = {}
with open(file_configuration, 'r') as stream:
    try:
        configuration = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:   
        print(exc)


def main(**kwargs):
    folder = kwargs.get("folder", f"{os.path.dirname(__file__)}/parts")
    folder = folder.replace("\\","/")
    
    kwargs["configuration"] = configuration
    print(f"running utility for: {folder}")
    create_recursive(**kwargs)

def create_recursive(**kwargs):
    folder = kwargs.get("folder", os.path.dirname(__file__))
    kwargs["folder"] = folder
    filter = kwargs.get("filter", "")
    #if folder exists
    if os.path.exists(folder):
        if filter in folder:
            counter = 0
            for item in os.listdir(folder):
                directory_absolute = os.path.join(folder, item)
                directory_absolute = directory_absolute.replace("\\","/")
                if os.path.isdir(directory_absolute):
                    #if working.yaml exists in the folder
                    if os.path.exists(os.path.join(directory_absolute, "working.yaml")):
                        kwargs["directory_absolute"] = directory_absolute
                        create(**kwargs)
                        counter += 1
                        if counter % 100 == 0:
                            print(f"    {counter} folders processed")
    else:
        print(f"no folder found at {folder}")

def create(**kwargs):
    directory_absolute = kwargs.get("directory_absolute", os.getcwd())    
    kwargs["directory_absolute"] = directory_absolute    
    generate(**kwargs)
    

def generate(**kwargs):    
    directory_absolute = kwargs.get("directory_absolute", os.getcwd())
    folder = kwargs.get("folder", os.getcwd())
    yaml_file = os.path.join(directory_absolute, "working.yaml")
    kwargs["yaml_file"] = yaml_file
    #load the yaml file
    details = {}
    with open(yaml_file, 'r') as stream:
        try:
            details = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:   
            print(exc)
    kwargs["details"] = details

    if details != {}:        
        #print(f"    generating for {directory_absolute}")
        #import from this folder
        # impotoomp_word from this files directory even if that isn't the cwd
        import sys
        sys.path.append(os.path.dirname(__file__))
        #import oomp_word
        
        ##### process part here



        

        #write back to yaml file
        with open(yaml_file, 'w') as outfile:
            yaml.dump(details, outfile, default_flow_style=False)
        


    else:
        print(f"no yaml file found in {directory_absolute}")    



if __name__ == '__main__':
    #folder is the path it was launched from
    
    kwargs = {}
    folder = os.path.dirname(__file__)
    #folder = "C:/gh/oomlout_oomp_builder/parts"
    folder = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
    #folder = "C:/gh/oomlout_oobb_version_4/things"
    #folder = "C:/gh/oomlout_oomp_current_version"
    kwargs["folder"] = folder
    overwrite = False
    kwargs["overwrite"] = overwrite
    main(**kwargs)