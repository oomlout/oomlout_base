
def get_table(**kwargs):
    data = kwargs.get("data","none")
    #data is an array of dicts or an array of lists
    #if it's an array of lists
    #if data is a list
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
