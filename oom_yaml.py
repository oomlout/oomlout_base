import yaml
import os
import oom_markdown

def load_yaml_directory(**kwargs):
    directory = kwargs['directory']
    return_value = {}
    yaml_files_to_add = ["working.yaml","working_manual.yaml","kicad/current_version/working/working.yaml","kicad/current_version/working/working_manual.yaml"]
    for yaml_file in yaml_files_to_add:
        yaml_file = os.path.join(directory, yaml_file)
        if os.path.exists(yaml_file):
            with open(yaml_file, 'r') as stream:
                try:
                    yaml_data = yaml.load(stream, Loader=yaml.FullLoader)
                    if yaml_data != None:
                        return_value.update(yaml_data)
                except Exception as exc:
                    print(exc)
                    return {}
                
        else:
            pass
            #print(f"yaml file not found: {yaml_file}")
    return return_value

def add_detail(**kwargs):    
    yaml_file = kwargs.get('yaml_file', "")
    detail = kwargs.get('detail', "")
    add_markdown = kwargs.get('add_markdown', False)
    oomp_replace = kwargs.get('oomp_replace', False)
    print(f"Adding detail {detail[0]} to {yaml_file}")
    #if yaml file doesn't exist create it
    if not os.path.exists(yaml_file):
        with open(yaml_file, 'w') as outfile:
            yaml.dump({}, outfile, default_flow_style=False)

    #load yaml
    with open(yaml_file, 'r') as stream:
        try:
            yaml_data = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(f"Error loading yaml file {yaml_file}")
            print(exc)
            return []
            
    #add details
    if yaml_data == None:
        yaml_data = {}
    yaml_data[detail[0]] =detail[1]
    #save yaml
    with open(yaml_file, 'w') as outfile:
        yaml.dump(yaml_data, outfile, default_flow_style=False)

    if add_markdown:
        #add markdown
        import copy
        new_details = copy.deepcopy(detail)
        new_details[0] = f"{detail[0]}_markdown"
        if oomp_replace:
            new_details[1] = oom_markdown.get_table_oomp_replace(data=detail[1])
        else:
            new_details[1] = oom_markdown.get_table(data=detail[1])
        add_detail(yaml_file=yaml_file, detail=[new_details[0], new_details[1]])

    return yaml_data