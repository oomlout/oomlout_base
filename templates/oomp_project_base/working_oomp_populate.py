
import copy
import os
import yaml


def build_oomp_id(d):
    fields = [
        d.get("classification", ""),
        d.get("type", ""),
        d.get("size", ""),
        d.get("color", ""),
        d.get("description_main", ""),
        d.get("description_extra", ""),
        d.get("manufacturer", ""),
        d.get("part_number", "")
    ]
    # Only include non-empty fields, join with underscores
    return '_'.join([str(f).strip().replace(' ', '_') for f in fields if f])

def main(**kwargs):
    # Define default input dict with all required fields
    default_input = {
        "classification": "helen",
        "type": "personal",
        "size": "chart",
        "color": "bribe_bank",
        "description_main": "",
        "description_extra": "",
        "manufacturer": "",
        "part_number": "",
        # Add any additional details here
    }
    
    
    #### define extra entries
    
    options = []
    if True:
        option = {}
        #reason 600 house points        
        option["theme"] = "unicorn"
        option["style"] = "rainbow_pastel"
        option["value_1"] = "tv_watching"
        option["value_2"] = "fish_and_chips_or_hamburgers"
        option["value_3"] = "billy_bobs_north_yorkshire_american_diner"
        options.append(option)
    

    extras = []
    for option in options:
        extra = copy.deepcopy(default_input)
        extra.update(option)
        extra["description_main"] = f"{option.get('theme', '')}_theme_{option.get('style', '')}_style"
        extra["description_extra"] = f"{option.get('value_1', '')}_{option.get('value_2', '')}_{option.get('value_3', '')}"
        extras.append(extra)



    # Loop over inputs
    for input_dict in extras:
        details = copy.deepcopy(default_input)
        details.update(input_dict)
        oomp_id = build_oomp_id(details)
        if not oomp_id:
            oomp_id = "default_empty"
        folder_path = os.path.join("parts_source", oomp_id)
        os.makedirs(folder_path, exist_ok=True)
        yaml_path = os.path.join(folder_path, "working.yaml")
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(details, f, allow_unicode=True)

# Call main automatically
if __name__ == "__main__":
    main()
