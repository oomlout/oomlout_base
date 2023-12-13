import os
# An oomp utility to:
# delete all the working,yaml files to cleanse before rebuilding from base.yaml 
# 
# This is part of OOMP the Oopen Organization Method For Parts. For more details: https://github.com/oomlout/oomp_base  


def main(**kwargs):
    recursive_through_parts(**kwargs)    
    
def recursive_through_parts(**kwargs):
    folder = kwargs.get("folder", os.path.dirname(__file__))
    kwargs["folder"] = folder
    for item in os.listdir(folder):
        item_absolute = os.path.join(folder, item)
        if os.path.isdir(item_absolute):
            #if base.yaml exists in the folder or working,yaml exists in the folder
            if os.path.exists(os.path.join(item_absolute, "base.yaml") or os.path.join(item_absolute, "working.yaml")):
                kwargs["directory"] = item_absolute
                process_part(**kwargs)

def process_part(**kwargs):
    directory = kwargs.get("directory", os.getcwd())    
    kwargs["directory"] = directory        
    print("Processing: {}".format(directory))

if __name__ == '__main__':
    #folder is the path it was launched from
    
    kwargs = {}
    folder = os.path.dirname(__file__)
    #folder = "C:/gh/oomlout_oomp_builder/parts"
    #folder = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
    #folder = "C:/gh/oomlout-organization/oomlout_oomp_current_version/parts"
    kwargs["folder"] = folder
    main(**kwargs)