
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
        "classification": "ai",
        "type": "data_source",
        "size": "calendar",
        "color": "date",
        "description_main": "",
        "description_extra": "",
        "manufacturer": "",
        "part_number": "",
        # Add any additional details here
    }
    
    
    #### define extra entries
    extras = []
    #iterate through all the days in a year in 2_29 format
    years = [0]
    months = [[1,31], [2,29], [3,31], [4,30], [5,31], [6,30], [7,31], [8,31], [9,30], [10,31], [11,30], [12,31]]
    month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    for year in years:
        for month, days in months:
            for day in range(1, days + 1):
                
                extra = {}
                date_str = str(f'{year}_{month}_{day}')
                extra["description_main"] = date_str
                extra["date"] = date_str
                extra["day"] = day
                extra["month"] = month
                extra["month_name"] = month_names.get(month, "")
                extra["year"] = year
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
