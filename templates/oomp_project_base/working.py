import oom_kicad


#process
#  locations set in working_parts.ods 
#  export to working_parts.csv
#  put components on the right side of the board
#  run this script

def main(**kwargs):
    board_file = "kicad/current_version/working/working.kicad_pcb"
    parts_file = "working_parts.csv"
    #load csv file
    import csv
    with open(parts_file, 'r') as f:
        reader = csv.DictReader(f)
        parts = [row for row in reader]


    oom_kicad.kicad_set_components(board_file=board_file, parts=parts, corel_pos=True, **kwargs)






if __name__ == '__main__':
    main()