import oom_kicad
import os
import oom_base

#find all the cdr files in the directory it was launched from and then run do_stuff(filename) to each one

def main_single_directory():
    #find all cdr files in the directory it was launched from
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".kicad_pcb"):
            #if filename doesnt include backup
            if "backup" not in filename.lower():
                print(f'Generating outputs for {filename}')
                oom_kicad.generate_outputs(filename=filename, computer="desktop" , overwrite=True, skip_oomp_folder=True)


def main_recursive():
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            filename = os.path.join(root, file)
            if filename.endswith(".kicad_pcb"):
                #if filename doesnt include backup
                if "backup" not in filename.lower():
                    print(f'Generating outputs for {filename}')
                    oom_kicad.generate_outputs(filename=filename, computer="desktop", overwrite=True, skip_oomp_folder=True)
                    svg_filename = filename.replace(".kicad_pcb", ".svg")
                    if os.path.isfile(svg_filename):
                        oom_base.image_svg_to_png(filename=svg_filename)                    




if __name__ == '__main__':
    main_recursive()