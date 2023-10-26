import os
import csv
import oom_base

def get_table_dict(**kwargs):
    data = kwargs.get("data","none")
    new_data = []
    new_data.append(["name","value"])
    for key in data:
        new_data.append([key,data[key]])
    return get_table(data=new_data)

def get_table_oomp_replace(**kwargs):
    import oomp
    oomp.load_parts(from_pickle=True)
    data = kwargs.get("data","none")
    for row in data:
        if "oomp_id" in row:
            oomp_id = row["oomp_id"]
            oomp_id = oomp_id.replace("oomp_","")
            if oomp_id in oomp.parts:
                oomp_part = oomp.parts[oomp_id]
                row["oomp_id"] = oomp_part["markdown_short"]
            else:
                print(f"oomp_id not found: {oomp_id}")
        else:
            print("no oomp_id column")

    return get_table(data=data)

def get_table(**kwargs):
    data = kwargs.get("data","none")
    #if each element of data is just a string make it a string in an array
    new_data = []
    for row in data:
        if type(row) == str:            
            new_data.append([row])
        else:
            new_data.append(row)
    data = new_data
    #go through all values in data and replace \n, \r and \n\r with <br>
    for row in data:
        #if row is a dict
        if type(row) == dict:
            for key in row:
                value = row[key]            
                value = value.replace("\n","<br>")
                value = value.replace("\r","<br>")
                value = value.replace("\n\r","<br>")
                row[key] = value
        #if row is a list
        if type(row) == list:
            for i in range(len(row)):
                value = row[i]       
                #if value is  a string
                if type(value) == str:     
                    value = value.replace("\n","<br>")
                    value = value.replace("\r","<br>")
                    value = value.replace("\n\r","<br>")
                    row[i] = value                
                elif type(value) == dict:
                    for key in value:
                        value2 = value[key]
                        value2 = value2.replace("\n","<br>")
                        value2 = value2.replace("\r","<br>")
                        value2 = value2.replace("\n\r","<br>")
                        value[key] = value2
                    row[i] = value
                #if value is an array of strings replace in all strings ad a <br> between the strings
                elif type(value) == list:
                    value = "<br>".join(str(value))
                    row[i] = value
                #if value is a dict
    #data is an array of dicts or an array of lists
    #if it's an array of lists
    #if data is a list
    if len(data) == 0:
        return "no data"
    #if it's a list of strings
    if type(data[0]) == str:
        #convert the list to a dict
        data_dict = []
        for row in data:
            data_dict.append({"name":row,"value":""})
        data = data_dict
    if type(data) == list:
        #if the first element is a list
        if type(data[0]) == list:
            #convert the list to a dict
            data_dict = []
            for row in data:
                if len(row) == 2:
                    data_dict.append({"name":row[0],"value":row[1]})
                else:
                    item = {}
                    for i in range(len(row)):
                        item.update({f"item{i}":row[i]})
                    data_dict.append(item)
            data = data_dict
    #if data is a dict
    #write a markup table with the keys as headings
    # and the values as the data
    #if data is a list of dicts
    return_value = ""
    return_value += "| "
    for key in data[0]:
        return_value += f"{key} | "
    return_value += "\n"
    return_value += "| "
    for key in data[0]:
        return_value += f"--- | "
    return_value += "\n"
    for row in data:
        return_value += "| "
        for key in row:
            return_value += f"{row[key]} | "
        return_value += "\n"                    
    return return_value
   
def get_link(**kwargs):
    link = kwargs.get("link","none")
    text = kwargs.get("text","none")
    if text == "none":
        text = link
    return_value = f'[{text}]({link})'
    return return_value

def get_link_image_scale(**kwargs):    
    image = kwargs.get("image","none")
    resolution = str(kwargs.get("resolution","140"))
    image_low_res = image
    image_low_res = image_low_res.replace(".png",f"_{resolution}.png")
    image_low_res = image_low_res.replace(".jpg",f"_{resolution}.jpg")
    image_low_res = image_low_res.replace(".jpeg",f"_{resolution}.jpeg")
    #get a markdown image that links to another image
    return_value = f"[![{image}]({image_low_res})]({image})"
    return return_value

### jinja2 template stuff

dir_oomlout_base = "c:/gh/oomlout_base"
dir_template = f"{dir_oomlout_base}/templates"

def generate_readme_project(**kwargs):
    import os
    directory = kwargs.get("directory",os.getcwd())
    directory_board = f"{directory}/kicad/current_version/working"
    template_file = f"{dir_template}/project_readme_template.md.j2"
    output_file = f"{directory}/readme.md"
    details = {}


    import oom_kicad
    oom_kicad.load_bom_into_yaml(directory=directory_board)



    #load details from working,yaml file    
    import yaml
    import oom_yaml
    details = oom_yaml.load_yaml_directory(directory=directory)
    
    
    
    
    files = []    
    #get a list of recursive files
    import glob
    files = glob.glob(f"{directory}/**/*.*", recursive=True)
    #replace all \\ with /
    for i in range(len(files)):
        files[i] = files[i].replace("\\","/")
    #remove the directory from the file name
    # replace \\ with / in directory
    directory = directory.replace("\\","/")
    for i in range(len(files)):
        files[i] = files[i].replace(f"{directory}/","")
    import copy
    files2 = copy.deepcopy(files)
    details["files"] = files2

    

    #oomp_parts_summary
    bom_file = f"{directory}/kicad/current_version/working/working_bom.csv"
    if os.path.exists(bom_file):
        files = []    
        #divider is a ;
        with open(bom_file, newline='' ) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                files.append(row)
        #make a new dict entry for each line
        new_data = []    
        oomp_yaml_file = "tmp/oomlout_oomp_part_src/parts.yaml"
        backup_yaml_file = "c:/gh/oomlout_base/tmp/oomlout_oomp_part_src/parts.yaml"
        oomp_parts = {}
        if os.path.exists(oomp_yaml_file):
            with open(oomp_yaml_file, 'r') as stream:
                print(f"loading oomp_yaml_file: {oomp_yaml_file}")
                try:
                    oomp_parts = yaml.load(stream, Loader=yaml.FullLoader)
                except yaml.YAMLError as exc:   
                    print(exc)
        elif os.path.exists(backup_yaml_file):
            with open(backup_yaml_file, 'r') as stream:
                print(f"loading backup_yaml_file: {backup_yaml_file}")
                try:
                    oomp_parts = yaml.load(stream, Loader=yaml.FullLoader)
                except yaml.YAMLError as exc:   
                    print(exc)
        else:
            print(f"oomp_yaml_file not found: {oomp_yaml_file}")
            

        for i in range(len(files)):
            footprint = files[i]
            #footprint is everything after the first _
            oomp_id = footprint["Footprint"].split("_",1)[1]
            index = footprint["Id"] 
            designator = footprint["Designator"]
            quantity = footprint["Quantity"]
            new_datum = {}
            #add index            
            new_datum.update({"index":index})
            new_datum.update({"designator":designator})
            new_datum.update({"quantity":quantity})
            try:
                oomp_markdown = oomp_parts[oomp_id]["markdown_full"]
            except:
                oomp_markdown = oomp_id
            new_datum.update({"oomp_id":oomp_markdown})
            new_data.append(new_datum)
        bom_table = get_table(data=new_data)
        details["oomp_parts_table"] = bom_table

    file_template = template_file
    file_output = output_file
    dict_data = details
    get_jinja2_template(file_template=file_template,file_output=file_output,dict_data=dict_data)


def add_files_to_dict_data(**kwargs):
    return oom_base.add_files_to_dict_data(**kwargs)

def get_jinja2_template(**kwargs):
    oom_base.get_jinja2_template(**kwargs)