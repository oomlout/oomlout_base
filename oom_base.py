





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