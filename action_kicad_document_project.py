import oom_kicad
import os


def main(**kwargs):
    #current working if not mentioned
    directory = kwargs.get("directory",os.getcwd())
    #print(f"directory is {directory}")
    for root, dirs, files in os.walk(directory):
        #go through all files        
        for file in files:
            #check for a brd file
            
            filename = os.path.join(root, file)
            #print(f"filename is {filename}")
            #don't do it if autosave or backup are in filename
            filter = ["autosave","backup"]
            if any(x in filename for x in filter):
                print(f"skipping {filename}")
            else:
                if file.endswith(".kicad_pcb"):
                    #print(f"processing {filename}")
                    oom_kicad.generate_outputs(filename=filename, computer="desktop")
                    pass








if __name__ == "__main__":
    main()



