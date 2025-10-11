import oomp
import copy

def main(**kwargs):
    load_parts(**kwargs)

def load_parts(**kwargs):
    make_files = kwargs.get("make_files", True)
    #print "loading parts" plus the module name get the module name from the filename using __name__
    print(f"  loading parts {__name__}")
    create_generic(**kwargs)

def create_generic(**kwargs):
    print(f"  creating sellers")
    parts = []

    part_details = {}
    part_details["classification"] = "personal"
    part_details["type"] = "helen"
    part_details["size"] = "school"
    part_details["color"] = "voting"
    part_details["description_main"] = "year_3"
    part_details["description_extra"] = ""
    part_details["manufacturer"] = ""
    part_details["part_number"] = ""

    default_empty = part_details.copy()

    people = {}
    person = {}
    person["id"] = "person_1"
    person["name"] = "Rayan"
    person["slogan"] = "You won't regret it!"
    person["style"] = "spotty"
    person["color"] = "pastel"
    people[person["id"]] = person




    for person in people:
        current = people[person]
        part = copy.deepcopy(part_details)        
        part["description_main"] = person
        
        name = current["name"]
        slogan = current["slogan"]
        style = current["style"]
        color = current["color"]

        prompts = []
        wordlist = ["Vote For", name, slogan]

        for words in wordlist:
            prompt_1 = f'please generate. A bold 3D block text design that says "{words}" in a playful but striking style, sized for a 3 wide by 2 tall landscape postcard. The design should avoid soft shading and instead use sharp angular planes with a limited {color}, making it screen-print friendly. The 3D text should look dynamic and fun, popping forward with strong outlines and a {style} pattern. The background should be plain white with no drop shadows. No gradients, only solid patches of colour. Make the design clean, bold, and eye-catching, with a balance between text and background so the message is clear. Square corners, no border. it must be 3x2 and on a plain white background with no drop shadow'
            prompts.append(prompt_1)


        #image
        if True:
            count = 1
            for prompt in prompts:
            #creating actions                
                actions = []
                action = {}
                #- command: 'new_chat'
                action["command"] = "new_chat"  
                action["description"] = f"rice image {current["name"]}"
                actions.append(action)
                #- command: 'query'
                    #text: 'can i get some pictures of tourist attractions in hx2 halifax uk, please ensure it is definietly in the uk and has the post code hx2?'
                action = {}
                action["command"] = "query"
                action["text"] = prompt
                action["delay"] = 60
                actions.append(action)
                
                action = {}
                #- command: 'save_image'
                action["command"] = "save_image_generated"  
                action["file_name"] = f"initial_generated_cgi.png"
                actions.append(action)


                #- command: 'add_image'
                action = {}
                action["command"] = "add_image"
                action["file_name"] = f"initial_generated_{count}.png"           
                actions.append(action)

                #close tab
                action = {}
                action["command"] = "close_tab"
                actions.append(action)

                base  = {}
                base["actions"] = copy.deepcopy(actions)
                file_test = f"initial_generated_{count}.png"
                base["file_test"] = file_test
                part[f"oomlout_ai_roboclick_{count}"] = base
                count += 1
        
        #trace
        if True:
            #trace file
            count = 1
            for prompt in prompts:
                if True:
                    actions = []

                    #wait_for_file initial_generation.png
                    action = {}
                    action["command"] = "wait_for_file"
                    action["file_name"] = f"initial_generated_{count}.png"                
                    actions.append(copy.deepcopy(action))

                    action = {}
                    action["command"] = "corel_trace_full"
                    action["file_source"] = f"source_files\\working_landscape\\working.cdr"
                    action["file_source_trace"] = f"initial_generated_{count}.png"
                    action["file_destination"] = f"trace_{count}.cdr"
                    action["max_dimension"] = 150
                    #cordinates 31,50
                    action["x"] = 75
                    action["y"] = 50
                    actions.append(copy.deepcopy(action))
                    
                    base  = {}
                    base["actions"] = copy.deepcopy(actions)
                    #the file that is created so skips if done
                    file_test = f"trace_{count}.png"
                    base["file_test"] = file_test
                    part["oomlout_corel_roboclick_1"] = base

        #trace
                

        
        
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


if __name__ == "__main__":
    # run the function
    load_parts()    
    