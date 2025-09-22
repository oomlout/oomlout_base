import oomp
import copy

def load_parts(**kwargs):
    make_files = kwargs.get("make_files", True)
    #print "loading parts" plus the module name get the module name from the filename using __name__
    print(f"  loading parts {__name__}")
    create_generic(**kwargs)

def create_generic(**kwargs):
    print(f"  creating sellers")
    parts = []

    part_details = {}
    part_details["classification"] = "game"
    part_details["type"] = "card"
    part_details["size"] = "whatnot"
    part_details["color"] = "stat_clash"
    part_details["description_main"] = "food_rice_types"
    part_details["description_extra"] = ""
    part_details["manufacturer"] = ""
    part_details["part_number"] = ""

    default_empty = part_details.copy()

    
    rice_types = {}

    rice_type_current = {}
    rice_type_current["name"] = "basmati"
    rice_type_current["name_proper"] = "Basmati"
    rice_type_current["description"] = "Long-grain aromatic rice from the Indian subcontinent, known for its fragrance and fluffy texture."
    rice_type_current["description_proper"] = "Long-Grain Aromatic Rice"
    rice_type_current["region"] = "India / Pakistan"
    rice_type_current["category"] = "Everyday / Table Rice"
    rice_type_current["index"] = "1"
    rice_types["basmati"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "jasmine"
    rice_type_current["name_proper"] = "Jasmine"
    rice_type_current["description"] = "Fragrant long-grain rice from Thailand, soft and slightly sticky when cooked."
    rice_type_current["description_proper"] = "Fragrant Long-Grain Rice"
    rice_type_current["region"] = "Thailand"
    rice_type_current["category"] = "Everyday / Table Rice"
    rice_type_current["index"] = "2"
    rice_types["jasmine"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "sona_masoori"
    rice_type_current["name_proper"] = "Sona Masoori"
    rice_type_current["description"] = "Lightweight medium-grain rice widely used in South Indian cuisine."
    rice_type_current["description_proper"] = "Medium-Grain Rice"
    rice_type_current["region"] = "India"
    rice_type_current["category"] = "Everyday / Table Rice"
    rice_type_current["index"] = "3"
    rice_types["sona_masoori"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "seeraga_samba"
    rice_type_current["name_proper"] = "Seeraga Samba"
    rice_type_current["description"] = "Tiny, fragrant rice often used for biryanis in Tamil Nadu."
    rice_type_current["description_proper"] = "Small Aromatic Grain"
    rice_type_current["region"] = "India"
    rice_type_current["category"] = "Everyday / Table Rice"
    rice_type_current["index"] = "4"
    rice_types["seeraga_samba"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "kalijira"
    rice_type_current["name_proper"] = "Kalijira"
    rice_type_current["description"] = "Also called 'baby basmati', a tiny fragrant rice from Bangladesh."
    rice_type_current["description_proper"] = "Tiny Aromatic Grain"
    rice_type_current["region"] = "Bangladesh"
    rice_type_current["category"] = "Everyday / Table Rice"
    rice_type_current["index"] = "5"
    rice_types["kalijira"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "domsiah"
    rice_type_current["name_proper"] = "Domsiah"
    rice_type_current["description"] = "Traditional aromatic Persian rice with long grains and fluffy texture."
    rice_type_current["description_proper"] = "Persian Long-Grain Rice"
    rice_type_current["region"] = "Iran"
    rice_type_current["category"] = "Everyday / Table Rice"
    rice_type_current["index"] = "6"
    rice_types["domsiah"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "gobindobhog"
    rice_type_current["name_proper"] = "Gobindobhog"
    rice_type_current["description"] = "Short-grain aromatic rice used in Bengali sweets and dishes."
    rice_type_current["description_proper"] = "Short Aromatic Grain"
    rice_type_current["region"] = "India"
    rice_type_current["category"] = "Everyday / Table Rice"
    rice_type_current["index"] = "7"
    rice_types["gobindobhog"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "calrose"
    rice_type_current["name_proper"] = "Calrose"
    rice_type_current["description"] = "Medium-grain rice developed in California, sticky and versatile."
    rice_type_current["description_proper"] = "Medium-Grain Rice"
    rice_type_current["region"] = "USA (California)"
    rice_type_current["category"] = "Everyday / Table Rice"
    rice_type_current["index"] = "8"
    rice_types["calrose"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "yumepirika"
    rice_type_current["name_proper"] = "Yumepirika"
    rice_type_current["description"] = "Premium short-grain rice from Hokkaido, Japan, known for its sweetness and stickiness."
    rice_type_current["description_proper"] = "Premium Short-Grain Rice"
    rice_type_current["region"] = "Japan"
    rice_type_current["category"] = "Everyday / Table Rice"
    rice_type_current["index"] = "9"
    rice_types["yumepirika"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "ponni"
    rice_type_current["name_proper"] = "Ponni"
    rice_type_current["description"] = "Medium-grain rice from South India, often used in everyday meals and biryanis."
    rice_type_current["description_proper"] = "Medium-Grain Rice"
    rice_type_current["region"] = "India"
    rice_type_current["category"] = "Everyday / Table Rice"
    rice_type_current["index"] = "10"
    rice_types["ponni"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "ofada"
    rice_type_current["name_proper"] = "Ofada"
    rice_type_current["description"] = "Distinctively flavored rice grown in Nigeria, often served with spicy stew."
    rice_type_current["description_proper"] = "Heirloom Rice"
    rice_type_current["region"] = "Nigeria"
    rice_type_current["category"] = "Everyday / Table Rice"
    rice_type_current["index"] = "11"
    rice_types["ofada"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "matta"
    rice_type_current["name_proper"] = "Matta (Palakkadan Rosematta)"
    rice_type_current["description"] = "Nutty, red-tinted rice from Kerala, India, rich in fiber."
    rice_type_current["description_proper"] = "Wholegrain Red Rice"
    rice_type_current["region"] = "India"
    rice_type_current["category"] = "Everyday / Table Rice"
    rice_type_current["index"] = "12"
    rice_types["matta"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "koshihikari"
    rice_type_current["name_proper"] = "Koshihikari"
    rice_type_current["description"] = "Famous Japanese short-grain rice prized for sushi."
    rice_type_current["description_proper"] = "Short-Grain Sushi Rice"
    rice_type_current["region"] = "Japan"
    rice_type_current["category"] = "Sushi / Japanese Specialty"
    rice_type_current["index"] = "13"
    rice_types["koshihikari"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "akitakomachi"
    rice_type_current["name_proper"] = "Akitakomachi"
    rice_type_current["description"] = "High-quality Japanese short-grain rice, sticky and sweet."
    rice_type_current["description_proper"] = "Short-Grain Rice"
    rice_type_current["region"] = "Japan"
    rice_type_current["category"] = "Sushi / Japanese Specialty"
    rice_type_current["index"] = "14"
    rice_types["akitakomachi"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "sasanishiki"
    rice_type_current["name_proper"] = "Sasanishiki"
    rice_type_current["description"] = "Classic Japanese sushi rice, light and less sticky than Koshihikari."
    rice_type_current["description_proper"] = "Sushi Rice"
    rice_type_current["region"] = "Japan"
    rice_type_current["category"] = "Sushi / Japanese Specialty"
    rice_type_current["index"] = "15"
    rice_types["sasanishiki"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "yamada_nishiki"
    rice_type_current["name_proper"] = "Yamada Nishiki"
    rice_type_current["description"] = "The premier sake-brewing rice variety of Japan."
    rice_type_current["description_proper"] = "Sake Rice"
    rice_type_current["region"] = "Japan"
    rice_type_current["category"] = "Sushi / Japanese Specialty"
    rice_type_current["index"] = "16"
    rice_types["yamada_nishiki"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "arborio"
    rice_type_current["name_proper"] = "Arborio"
    rice_type_current["description"] = "Popular Italian short-grain rice, creamy when cooked, perfect for risotto."
    rice_type_current["description_proper"] = "Risotto Rice"
    rice_type_current["region"] = "Italy"
    rice_type_current["category"] = "Risotto / Italian"
    rice_type_current["index"] = "17"
    rice_types["arborio"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "carnaroli"
    rice_type_current["name_proper"] = "Carnaroli"
    rice_type_current["description"] = "High-starch Italian rice variety known as the 'king of risotto'."
    rice_type_current["description_proper"] = "Risotto Rice"
    rice_type_current["region"] = "Italy"
    rice_type_current["category"] = "Risotto / Italian"
    rice_type_current["index"] = "18"
    rice_types["carnaroli"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "vialone_nano"
    rice_type_current["name_proper"] = "Vialone Nano"
    rice_type_current["description"] = "Medium-grain risotto rice from Veneto, Italy, with excellent absorption."
    rice_type_current["description_proper"] = "Risotto Rice"
    rice_type_current["region"] = "Italy"
    rice_type_current["category"] = "Risotto / Italian"
    rice_type_current["index"] = "19"
    rice_types["vialone_nano"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "baldo"
    rice_type_current["name_proper"] = "Baldo"
    rice_type_current["description"] = "Versatile Italian rice, slightly longer than Arborio, used in risotto and salads."
    rice_type_current["description_proper"] = "Medium-Grain Rice"
    rice_type_current["region"] = "Italy / Turkey"
    rice_type_current["category"] = "Risotto / Italian"
    rice_type_current["index"] = "20"
    rice_types["baldo"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "roma"
    rice_type_current["name_proper"] = "Roma"
    rice_type_current["description"] = "Italian rice variety with round grains, used in risotto and desserts."
    rice_type_current["description_proper"] = "Round-Grain Rice"
    rice_type_current["region"] = "Italy"
    rice_type_current["category"] = "Risotto / Italian"
    rice_type_current["index"] = "21"
    rice_types["roma"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "bomba"
    rice_type_current["name_proper"] = "Bomba"
    rice_type_current["description"] = "Spanish short-grain rice famous for paella, absorbs liquid without breaking."
    rice_type_current["description_proper"] = "Paella Rice"
    rice_type_current["region"] = "Spain"
    rice_type_current["category"] = "Paella / Spanish"
    rice_type_current["index"] = "22"
    rice_types["bomba"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "calasparra"
    rice_type_current["name_proper"] = "Calasparra"
    rice_type_current["description"] = "Protected designation Spanish rice with exceptional absorption for paella."
    rice_type_current["description_proper"] = "Paella Rice"
    rice_type_current["region"] = "Spain"
    rice_type_current["category"] = "Paella / Spanish"
    rice_type_current["index"] = "23"
    rice_types["calasparra"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "senia"
    rice_type_current["name_proper"] = "Senia"
    rice_type_current["description"] = "Spanish short-grain rice used in traditional Valencian paella."
    rice_type_current["description_proper"] = "Paella Rice"
    rice_type_current["region"] = "Spain"
    rice_type_current["category"] = "Paella / Spanish"
    rice_type_current["index"] = "24"
    rice_types["senia"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "bahia"
    rice_type_current["name_proper"] = "Bahia"
    rice_type_current["description"] = "Another classic Spanish rice for paella, round grains with good absorption."
    rice_type_current["description_proper"] = "Paella Rice"
    rice_type_current["region"] = "Spain"
    rice_type_current["category"] = "Paella / Spanish"
    rice_type_current["index"] = "25"
    rice_types["bahia"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "carolino"
    rice_type_current["name_proper"] = "Carolino"
    rice_type_current["description"] = "Portuguese medium-grain rice, used in soupy rice dishes like arroz de marisco."
    rice_type_current["description_proper"] = "Medium-Grain Rice"
    rice_type_current["region"] = "Portugal"
    rice_type_current["category"] = "Regional European"
    rice_type_current["index"] = "26"
    rice_types["carolino"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "camargue_red"
    rice_type_current["name_proper"] = "Camargue Red"
    rice_type_current["description"] = "Nutty wholegrain red rice grown in the Camargue region of France."
    rice_type_current["description_proper"] = "Wholegrain Red Rice"
    rice_type_current["region"] = "France"
    rice_type_current["category"] = "Specialty (Red & Black)"
    rice_type_current["index"] = "27"
    rice_types["camargue_red"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "bhutanese_red"
    rice_type_current["name_proper"] = "Bhutanese Red"
    rice_type_current["description"] = "Hearty red rice from Bhutan, semi-milled so it cooks faster."
    rice_type_current["description_proper"] = "Wholegrain Red Rice"
    rice_type_current["region"] = "Bhutan"
    rice_type_current["category"] = "Specialty (Red & Black)"
    rice_type_current["index"] = "28"
    rice_types["bhutanese_red"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "red_cargo"
    rice_type_current["name_proper"] = "Red Cargo"
    rice_type_current["description"] = "Unmilled red rice from Thailand, chewy with a nutty flavor."
    rice_type_current["description_proper"] = "Wholegrain Red Rice"
    rice_type_current["region"] = "Thailand"
    rice_type_current["category"] = "Specialty (Red & Black)"
    rice_type_current["index"] = "29"
    rice_types["red_cargo"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "black"
    rice_type_current["name_proper"] = "Black (Forbidden)"
    rice_type_current["description"] = "Ancient black rice from China, high in antioxidants and nutty flavor."
    rice_type_current["description_proper"] = "Wholegrain Black Rice"
    rice_type_current["region"] = "China"
    rice_type_current["category"] = "Specialty (Red & Black)"
    rice_type_current["index"] = "30"
    rice_types["black"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "thai_black_sticky"
    rice_type_current["name_proper"] = "Thai Black Sticky"
    rice_type_current["description"] = "Glutinous black rice from Thailand, used in desserts."
    rice_type_current["description_proper"] = "Glutinous Black Rice"
    rice_type_current["region"] = "Thailand"
    rice_type_current["category"] = "Specialty (Red & Black)"
    rice_type_current["index"] = "31"
    rice_types["thai_black_sticky"] = rice_type_current

    rice_type_current = {}
    rice_type_current["name"] = "glutinous"
    rice_type_current["name_proper"] = "Glutinous (Sticky)"
    rice_type_current["description"] = "High-amylopectin rice that turns sticky when cooked, essential in Southeast Asian cuisine."
    rice_type_current["description_proper"] = "Sticky Rice"
    rice_type_current["region"] = "Southeast Asia"
    rice_type_current["category"] = "Glutinous / Sticky"
    rice_type_current["index"] = "32"
    rice_types["glutinous"] = rice_type_current

    # back card
    rice_type_current = {}
    rice_type_current["name"] = "back"
    rice_type_current["name_proper"] = "Back"
    rice_type_current["description"] = "Card back design with rice-themed abstract pattern."
    rice_type_current["description_proper"] = "Card Back"
    rice_type_current["region"] = "N/A"
    rice_type_current["category"] = "Back"
    rice_type_current["index"] = "33"
    rice_types["back"] = rice_type_current

    for rice in rice_types:
        current = rice_types[rice]
        part = default_empty.copy()
        part.update(current)

        part["description_extra"] = current["name"]
        parts.append(part)


        #trace
        if True:
            #trace file
            if True:
                actions = []

                #wait_for_file initial_generation.png
                action = {}
                action["command"] = "wait_for_file"
                action["file_name"] = f"initial_generated_card_full.png"                
                actions.append(copy.deepcopy(action))

                action = {}
                action["command"] = "corel_trace_full"
                action["file_source"] = f"source_files\\working_card_1\\working.cdr"
                action["file_source_trace"] = f"initial_generated_card_full.png"
                action["file_destination"] = f"trace_card_full.cdr"
                action["max_dimension"] = 90
                #cordinates 31,50
                action["x"] = 31
                action["y"] = 50
                actions.append(copy.deepcopy(action))

                base  = {}
                base["actions"] = copy.deepcopy(actions)
                #the file that is created so skips if done
                file_test = "trace.png"
                base["file_test"] = file_test
                part["oomlout_corel_roboclick_1"] = base
    
        #generate image
        if True:
            #the ai generation
            actions = []  
            #image
            if True:
            #creating actions                
                
                action = {}
                #- command: 'new_chat'
                action["command"] = "new_chat"  
                action["description"] = f"rice image {current["name"]}"
                actions.append(action)
                #- command: 'query'
                    #text: 'can i get some pictures of tourist attractions in hx2 halifax uk, please ensure it is definietly in the uk and has the post code hx2?'
                action = {}
                action["command"] = "query"
                action["text"] = f"I'm making a game about different rices! for that I need a cgi high detail and spec with awesome lighting anthropomorphised chibi picture! can i get a generic prompt for doing that I'd like the main rice grain to be big and in the centre and then surrounded by things that help describe it like the type of rice it is where it's from things like that. also it needs to be suare. take all the time you'd like"
                action["delay"] = 240
                actions.append(action)
                
                #- command: 'add_image'
                action = {}
                action["command"] = "add_image"
                action["file_name"] = f"search_result_1.jpg"           
                ##actions.append(action)

                #- command: 'query'
                #text: 'can you tell me how you would describe a chibi style sticker of a tourist attraction and add HX2 to it, as well as the text of the attractions name'
                action = {}
                action["command"] = "query"
                action["text"] = f"that is so so so great! can you spend some time learning about {current} rice, things like what it's used for and where it's from and insert those details into the prompt you made for me before. I want the image to really represent the rice type and be super cute and chibi style. take all the time you need"
                action["delay"] = 240
                actions.append(action)
                
                #- command: 'add_image'
                action = {}
                action["command"] = "add_image"
                action["file_name"] = f"search_result_1.jpg"           
                #actions.append(action)
                
                #- command: 'query'
                action = {}
                action["command"] = "query"
                #action["text"] = "awesome make the full image using the uploaded photo as inspiration! Remember 3:2 landscape ratio! It must be landscape and 3 wide and 2 tall"
                action["text"] = "awesome Generate it for me please remember it needs to be square proporitions 1:1 and high detail and spec with awesome lighting"
                actions.append(action)

                action = {}
                #- command: 'save_image'
                action["command"] = "save_image_generated"  
                action["file_name"] = f"initial_generated_cgi.png"
                actions.append(action)


                #- command: 'add_image'
                action = {}
                action["command"] = "add_image"
                action["file_name"] = f"initial_generated_cgi.png"           
                actions.append(action)


                #- command: 'query'
                action = {}
                action["command"] = "query"
                #action["text"] = "awesome make the full image using the uploaded photo as inspiration! Remember 3:2 landscape ratio! It must be landscape and 3 wide and 2 tall"
                action["text"] = "I love it so much! can I also get a version of that image in a more vectorized version that has a limited color palette to make it good for screen printing? don't include any words or letters."
                actions.append(action)

                action = {}
                #- command: 'save_image'
                action["command"] = "save_image_generated"  
                action["file_name"] = f"initial_generated_vector.png"
                actions.append(action)


                #- command: 'query'
                action = {}
                action["command"] = "query"
                #action["text"] = "awesome make the full image using the uploaded photo as inspiration! Remember 3:2 landscape ratio! It must be landscape and 3 wide and 2 tall"
                action["text"] = f"this is all great! now time to do some research!. I need ratings from 1 to 10 based on how conducive {current["name"]} rice is. These are the categories. Grain Length, Aroma, Stickiness, Absorption, Price, Overall Score. take as much time as you need."
                action["delay"] = 240
                actions.append(action)

                #- command: 'query'
                action = {}
                action["command"] = "query" 
                
                #action["text"] = "awesome make the full image using the uploaded photo as inspiration! Remember 3:2 landscape ratio! It must be landscape and 3 wide and 2 tall"
                action["text"] = f"You're a research star! I need that data in a way that i can easily put it into python so please format it like this <<<tag for copy>>> details['{current["name"]}'] = {{'grain_length': 8, 'aroma': 9, 'stickiness': 6, 'absorption': 7, 'price': 5, 'overall_score': 7}} <<<tag for copy>>> and nothing else. "
                actions.append(action)

                action = {}
                action["command"] = "ai_save_text"
                action["file_name_full"] = f"full_text.txt"
                action["file_name_clip"] = f"scores.py"
                action["clip"] = "<<<tag for copy>>>"
                actions.append(action)

                #close tab
                action = {}
                action["command"] = "close_tab"
                actions.append(action)

                base  = {}
                base["actions"] = copy.deepcopy(actions)
                file_test = "scores.py"
                base["file_test"] = file_test
                part["oomlout_ai_roboclick"] = base


    print(f"    found {len(parts)} parts")

    oomp.add_parts(parts, **kwargs)


if __name__ == "__main__":
    # run the function
    load_parts()    
    