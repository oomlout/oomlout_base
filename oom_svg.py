import os
import subprocess

def svg_dict_replace_simple(**kwargs):
    svg_infile = kwargs.get('svg_infile',"")
    svg_outfile = kwargs.get('svg_outfile',"")
    if svg_infile == "":
        print("No svg file specified")
        return
    svg_dict = kwargs.get('svg_dict',{})
    #load svg_infile into a string check if the file exists
    if not os.path.exists(svg_infile):
        print(f"File {svg_infile} does not exist")
        return
    with open(svg_infile, "r") as infile:
        svg_string = infile.read()
    #loop through svg_dict and replace the keys with the values
    for key in svg_dict:
        value = svg_dict[key].get("name","")
        search_string = f"%%{key}%%"
        if search_string in svg_string:
            x=1
        else:
            x=2
        svg_string = svg_string.replace(search_string, value)


    #write the svg_string to svg_outfile create directory if it doesn't exist
    directory = os.path.dirname(svg_outfile)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(svg_outfile, "w") as outfile:
        outfile.write(svg_string)
        print(f"writing {svg_outfile}")

def svg_dict_replace(**kwargs):
    svg_infile = kwargs.get('svg_infile',"")
    svg_outfile = kwargs.get('svg_outfile',"")
    if svg_infile == "":
        print("No svg file specified")
        return
    svg_dict = kwargs.get('svg_dict',{})
    #load svg_infile into a string check if the file exists
    if not os.path.exists(svg_infile):
        print(f"File {svg_infile} does not exist")
        return
    with open(svg_infile, "r") as infile:
        svg_string = infile.read()
    #loop through svg_dict and replace the keys with the values
    
    #extract all strings between %% and %% in svg string just te text between %%
    svg_string_list = svg_string.split("%%")
    svg_string_list = svg_string_list[1::2]
    #loop through svg_string_list and replace the keys with the values
    for key in svg_string_list:
        #split based on colon
        key_list = key.split(":")
        #replace key with that value layered from the svg_dict
        value = svg_dict
        for key2 in key_list:
            value = value.get(key2,{})
        #replace value in svg_string        
        search_string = f"%%{key}%%"
        if value == {}:
            value = ""
        replace_string = value 
        svg_string = svg_string.replace(search_string, replace_string)


    #write the svg_string to svg_outfile create directory if it doesn't exist
    directory = os.path.dirname(svg_outfile)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(svg_outfile, "w") as outfile:
        outfile.write(svg_string)
        print(f"writing {svg_outfile}")


def svg_make_pdf(**kwargs):
    kwargs["file_type"] = "pdf"
    svg_make_file(**kwargs)

def svg_make_png(**kwargs):
    kwargs["file_type"] = "png"
    svg_make_file(**kwargs)

def svg_make_file(**kwargs):
    export_dpi = kwargs.get('export_dpi',"")
    file_type = kwargs.get('file_type',"pdf")
    file_in = kwargs.get('file_in',"")
    file_out = kwargs.get('file_out',"")
    if file_out == "":
        file_out = file_in.replace(".svg", f".{file_type}")
    #executeString = f"inkscape.exe --export-pdf-version=1.4 --export-text-to-path --export-filename=\"{file_out}\" \"{file_in}\""
    executeString = f'inkscape.exe --export-type="{file_type}" --export-filename="{file_out}"'
    if export_dpi != "":
        executeString += f' --export-dpi="{export_dpi}"'
    executeString += f'  "{file_in}"'
    print(f"converting to {file_type} {file_out}")
    os.system(executeString)