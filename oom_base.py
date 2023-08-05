import os

#image manipulation
def generate_image(**kwargs):
    filename = kwargs['filename']
    resolution = kwargs['resolution']
    overwrite = kwargs.get('overwrite', False)
    file_out = filename.split(".")[0] + "_" + str(resolution) + "." + filename.split(".")[1]
    #skip if overwrite is false and the file already exists
    if not overwrite:
        if os.path.isfile(file_out):
            return
    
    #if the image is already a resized on skip it chjeck for all numbers 100 or more
    if "_" in filename:
        if filename.split("_")[-1].split(".")[0].isdigit():
            if int(filename.split("_")[-1].split(".")[0]) >= 100:
                return
    
    #open the image file png or jpg
    from PIL import Image
    try:
        im = Image.open(filename)
        #scale the image so the largest side is reolution pixels wide
        width, height = im.size
        if width > height:
            scale = resolution / width
        else:
            scale = resolution / height
        new_width = int(width * scale)
        new_height = int(height * scale)
        im = im.resize((new_width, new_height), Image.ANTIALIAS)
        #save the image
        im.save(file_out)
    except:
        print("Error with image: " + filename)
        pass

# string manipulation

def remove_special_characters(string):
    symbol_name = string
    symbol_name = symbol_name.replace('/', '_')
    symbol_name = symbol_name.replace('\\', '_')
    symbol_name = symbol_name.replace(':', '_')
    symbol_name = symbol_name.replace('*', '_')
    symbol_name = symbol_name.replace('?', '_')
    symbol_name = symbol_name.replace('"', '_')
    symbol_name = symbol_name.replace('<', '_')
    symbol_name = symbol_name.replace('>', '_')
    symbol_name = symbol_name.replace('|', '_')
    symbol_name = symbol_name.replace('-', '_')        
    symbol_name = symbol_name.replace('+', '_')
    symbol_name = symbol_name.replace(' ', '_')
    symbol_name = symbol_name.replace('.', '_')
    symbol_name = symbol_name.replace('__', '_')
    symbol_name = symbol_name.replace('__', '_')
    symbol_name = symbol_name.replace('__', '_')
    symbol_name = symbol_name.replace('__', '_')
    return symbol_name




# data manipulation

#yaml to readme
def yaml_to_markdown(**kwargs):
    readme = ""
    yaml_dict = kwargs['yaml_dict']
    #if yaml_dict is an array take element 
    if type(yaml_dict) is list:
        yaml_dict = yaml_dict[0]
    #make a table with each yaml value key as a column value as the other
    #add header
    readme += "| Key | Value |  \n"
    readme += "| --- | --- |  \n"
    for key in yaml_dict:
        readme += "| " + key + " | " + str(yaml_dict[key]) + " |  \n"
        

    return readme