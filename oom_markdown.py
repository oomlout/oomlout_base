import os

def get_table_dict(**kwargs):
    data = kwargs.get("data","none")
    new_data = []
    new_data.append(["name","value"])
    for key in data:
        new_data.append([key,data[key]])
    return get_table(data=new_data)


def get_table(**kwargs):
    data = kwargs.get("data","none")
    #data is an array of dicts or an array of lists
    #if it's an array of lists
    #if data is a list
    if len(data) == 0:
        return "no data"
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
    directory = kwargs.get("directory","")
    template_file = f"{dir_template}/project_readme_template.md.j2"
    output_file = f"{directory}/readme.md"
    details = {}
    #load details from working,yaml file
    import yaml
    with open(f"{directory}/working.yaml", 'r') as stream:
        try:
            details = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
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


    #load working_bom.csv into an array
    import csv
    bom_file = f"{directory}/kicad/current_version/working/working_bom.csv"
    if os.path.exists(bom_file):
        files = []    
        #divider is a ;
        with open(bom_file, newline='' ) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                files.append(row)
        #replace footprint with link
        github_base_part = "https://github.com/oomlout/oomlout_oomp_part_src/tree/main/parts"
        for i in range(len(files)):
            footprint = files[i]["Footprint"]
            #footprint is everything after the first _
            footprint = footprint.split("_",1)[1]
            link = f"{github_base_part}/{footprint}"
            full_link = get_link(link=link,text=footprint)
            files[i]["Footprint"] = full_link
        bom_table = get_table(data=files)
        details["bom_table"] = bom_table

    #load working_parts.csv
    if os.path.exists(f"{directory}/working_parts.csv"):
        files = []    
        with open(f"{directory}/working_parts.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                files.append(row)
        #add link to oomp_key
        github_base_part = "https://github.com/oomlout/oomlout_oomp_part_src/tree/main/parts"
        for i in range(len(files)):
            oomp_key = files[i]["oomp_key"]
            key = oomp_key.replace("oomp_","")
            link = f"{github_base_part}/{oomp_key}"
            full_link = get_link(link=link,text=oomp_key)
            files[i]["oomp_key"] = full_link

        parts_table = get_table(data=files)
        details["parts_table"] = parts_table     
    
    file_template = template_file
    file_output = output_file
    dict_data = details
    get_jinja2_template(template_file=file_template,output_file=file_output,dict_data=dict_data)



def get_jinja2_template(**kwargs):
    file_template = kwargs.get("template_file","")
    file_output = kwargs.get("output_file","")
    dict_data = kwargs.get("dict_data",{})

    markdown_string = ""
    with open(file_template, "r") as infile:
        markdown_string = infile.read()
    ##### sanitize part
    import copy
    data2 = copy.deepcopy(dict_data)

    import jinja2    

    markdown_string = jinja2.Template(markdown_string).render(p=data2)
    with open(file_output, "w") as outfile:
        outfile.write(markdown_string)
        print(f"jinja2 template file written: {file_output}")

