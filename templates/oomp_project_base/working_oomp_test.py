import oomp
import copy
import oomlout_roboclick

def main(**kwargs):
    load_parts(**kwargs)

def load_parts(**kwargs):
    make_files = kwargs.get("make_files", True)
    #print "loading parts" plus the module name get the module name from the filename using __name__
    print(f"  loading parts {__name__}")
    create_generic(**kwargs)

def create_generic(**kwargs):
    print(f"  loading parts from part_source")
    things = {}    
    
    #load parts from parts_source directory
    directory_source = "parts_source"
    import os
    if not os.path.exists(directory_source):
        print(f"      directory {directory_source} does not exist, creating it")
        #create it
        os.makedirs(directory_source)
    directories = os.listdir(directory_source)
    for directory  in directories:
        directory_full = f"{directory_source}/{directory}"
        filenames = os.listdir(f"{directory_full}")
        for filename in filenames:
            import yaml
            #go through directories and load working.yaml files
            # only load .yaml files
            if "working.yaml" in filename:
                file_path = os.path.join(directory_full, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = yaml.safe_load(file)
                    thing_details = {}
                    for deet in data:
                        thing_details[deet] = data[deet]
                    things[directory] = thing_details
    
    
    default_empty = {}
    #if adding things by default, currently handled in the web form submission
    if True:
        # default_empty["classification"] = ""
        # default_empty["type"] = ""
        # default_empty["size"] = ""
        # default_empty["color"] = ""
        # default_empty["description_main"] = ""
        # default_empty["description_extra"] = ""
        # default_empty["manufacturer"] = ""
        # default_empty["part_number"] = ""
        words = ["Happy", "Mother's", "Day"]
        default_empty["words"] = words
        default_empty["animal"] = "donkey"

    parts = []

    for thing in things:
        current = things[thing]                
        #name stuff
        part = copy.deepcopy(default_empty)
        part.update(current)
        part["name"] = thing
        part["name_space"] = thing.replace("_", " ")
        part["name_proper"] = part["name_space"].title()
        part["name_upper"] = part["name_space"].upper()
        
        #convert "oomp_classification to just classification
        details_list = ["classification", "type", "size", "color", "description_main", "description_extra", "manufacturer", "part_number"]
        for detail in details_list:
            key = f"oomp_{detail}"
            if key in current:
                part[detail] = current[key]
                part.pop(key, None)


        folder = oomlout_roboclick.get_directory(part)   
        part["directory"] = folder  
        url_chat = oomlout_roboclick.get_url(part)   
        part["url_chat"] = url_chat
        count = 0

        mode_ai_wait = "fast"
        #mode_ai_wait = "slow"


        #icon
        if False:
            count += 1            
            action_type = "ai" # "corel"
            
            #action_name = f"create_icon"
            action_name = f"step_{count}_create_icon"
            
            file_test = f"initial_generated.png" 
            #file_test = "tag" #(creates a tag at the end)

            actions = []
            
            #### action 1
            action = {}
            action["command"] = "ai_skill_image_laser_cut_logo_full"            
            action["file_destination"] = file_test
            #action["file_destination"] = f"intial_generated_icon.png"
            detail = "detail"
            image_detail = f"an image of {detail}"
            action["image_detail"] = image_detail
            #mode_ai_wait fast
            action["mode_ai_wait"] = mode_ai_wait
            actions.append(copy.deepcopy(action))

            oomlout_roboclick.add_action(part=part, action_type=action_type, action_name=action_name, actions=actions, file_test=file_test)

        #prompt bubble letter
        if True:
            # prompt change
            prompts = []
            prompts.append({"folder_name" : "prompt\\prompt_bubble_letter_1", "delay" : "60"})
            #prompts.append({"file_name" : "prompt\\prompt_bubble_letter_1\\working_2.md", "delay" : "60"})
            words = part.get("words", [])
            word_count = len(words)
            for i in range(word_count):            
                word = words[i]
                prompts.append({"text" : f"Awesome fill in the json template with {word}"})
                prompts.append({"file_name_image" : f"initial_generated_{i+1}.png", "text" : f"Generate for it take all the time you need", "delay" : "60"})

            count = ai_query_from_prompts(part,prompts,mode_ai_wait, count)       

        #prompt image
        if True:
            # prompt change
            prompts = []
            prompts.append({"folder_name" : "prompt\\prompt_image_main_1", "delay" : "60"})                        
            prompts.append({"file_name_image" : f"image_main.png", "text" : f"Generate it take all the time you need", "delay" : "60"})
            count = ai_query_from_prompts(part,prompts,mode_ai_wait, count)       

        #cover_background
        #prompt image
        if True:
            # prompt change
            prompts = []
            prompts.append({"folder_name" : "prompt\\prompt_image_cover_background_1", "delay" : "60"})                        
            prompts.append({"file_name_image" : f"image_cover_background.png", "text" : f"Generate it take all the time you need", "delay" : "60"})
            count = ai_query_from_prompts(part,prompts,mode_ai_wait, count)       


        #internal border
        #prompt image
        if True:
            # prompt change
            prompts = []
            prompts.append({"folder_name" : "prompt\\prompt_inside_border_1", "delay" : "60"})                        
            prompts.append({"file_name_image" : f"image_inside_border.png", "text" : f"Generate it take all the time you need", "delay" : "60"})
            count = ai_query_from_prompts(part,prompts,mode_ai_wait, count)       

        #logo back
        #prompt image
        if True:
            # prompt change
            prompts = []
            prompts.append({"folder_name" : "prompt\\prompt_logo_back_1", "delay" : "60"})                        
            prompts.append({"file_name_image" : f"image_logo_back.png", "text" : f"Generate it take all the time you need", "delay" : "60"})
            count = ai_query_from_prompts(part,prompts,mode_ai_wait, count)       



        #trace
        if True:    
            words = part.get("words")        
            files_to_trace = []
            for i in range(len(words)):
                files_to_trace.append(f"initial_generated_{i+1}.png")
            files_to_trace.append("image_main.png")
            files_to_trace.append("image_cover_background.png")
            files_to_trace.append("image_inside_border.png")
            files_to_trace.append("image_logo_back.png")

            for file_to_trace in files_to_trace:
                count += 1            
                action_type = "ai" # "corel"
                
                action_name = f"create_icon"
                #action_name = f"step_{count}_create_icon"
                
                #file_test = f"intial_generated.png" 
                file_test = "tag" #(creates a tag at the end)

                file_name_source = f"{file_to_trace}"
                file_name_trace = f"{file_to_trace.replace('.png', '_trace.cdr')}"

                ### action 1
                # wait_for_file
                actions = []
                action = {}
                action["command"] = "wait_for_file"
                action["file_name"] = file_name_source
                actions.append(copy.deepcopy(action))

                ### action 2
                # corel trace_full
                action = {}
                action["command"] = "corel_trace_full"
                action["file_source"] = f"template\\blank_square_100_mm_width_100_mm_height\\working.cdr"
                action["file_source_trace"] = file_name_source
                action["file_destination"] = file_name_trace
                action["max_dimension"] = 95
                action["remove_background_color_from_entire_image"] = True
                #add color to border, logo
                if "inside_border" in file_to_trace or "logo_back" in file_to_trace:
                    action["number_of_colors"] = 2
                #cordinates 31,50
                action["x"] = 50
                action["y"] = 50
                actions.append(copy.deepcopy(action))
                
                file_test = file_name_trace.replace(".cdr", ".png")
                oomlout_roboclick.add_action(part=part, action_type=action_type, action_name=action_name, actions=actions, file_test=file_test)
        
        parts.append(part)
    



    oomp.add_parts(parts, **kwargs)

    #dd file copy
    for part in parts:
        file_copies = part.get("file_copy", [])
        if file_copies != []:
            for file_copy in file_copies:
                directory = part.get("directory", "")
                if directory != "":
                    file_source = f"{file_copy["file_source"]}"
                    file_destination = f"{directory}\\{file_copy["file_destination"]}"
                    import shutil
                    print(f"      copying {file_source} to {file_destination}")
                    try:
                        shutil.copyfile(file_source, file_destination)
                    except Exception as e:
                        print(f"      error copying file: {e}") 

    import time
    time.sleep(2)

def ai_query_from_prompts(part,prompts,mode_ai_wait, count):
    count += 1            
    action_type = "ai" # "corel"
    action_name = f"create_prompt_verbose"

    #default to a tag but if an image is created use that instead
    file_test = "tag" #(creates a tag at the end)

    actions = []
    
    ### action 1
    # new chat
    action = {}
    #- command: 'new_chat'
    action["command"] = "new_chat"  
    action["description"] = f"{action_name}"
    actions.append(action)
    
    ### action 2
    
    
    
    for prompt in prompts:                
        file_name_image = prompt.get("file_name_image", "")
        prompt.pop("file_name_image", None)
    
        action = {}
        action.update(copy.deepcopy(prompt))
        action["command"] = "ai_query"
        action["mode_ai_wait"] = mode_ai_wait
        actions.append(action)
    
        if file_name_image != "":
            action = {}
            #- command: 'save_image'
            action["command"] = "save_image_generated"  
            action["file_name"] = file_name_image
            action["mode_ai_wait"] = mode_ai_wait
            actions.append(action)
            #if image is created use that rather than tag
            file_test = file_name_image

    #close tab
    action = {}
    action["command"] = "close_tab"
    actions.append(action)

    oomlout_roboclick.add_action(part=part, action_type=action_type, action_name=action_name, actions=actions, file_test=file_test)  
    return count       


if __name__ == "__main__":
    # run the function
    load_parts()    
    