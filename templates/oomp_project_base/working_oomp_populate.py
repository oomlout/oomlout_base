
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
        "type": "school",
        "size": "general",
        "color": "certificate",
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
        option["reason"] = "600 House Points"
        option["theme"] = "lady_birds"
        option["style"] = "garden_with_lots_of_bugs"
        option["person"] = "Laila"
        options.append(option)
    

    extras = []
    for option in options:
        extra = copy.deepcopy(default_input)
        extra.update(option)
        extra["description_main"] = extra["theme"]
        extra["description_extra"] = extra["consequence"]
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
