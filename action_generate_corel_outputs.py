import oom_corel
import os

#find all the cdr files in the directory it was launched from and then run do_stuff(filename) to each one

def main_single_directory():
    #find all cdr files in the directory it was launched from
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".cdr"):
            #if filename doesnt include backup
            if "backup" not in filename.lower():
                print(f'Generating outputs for {filename}')
                oom_corel.generate_outputs(filename=filename, overwrite=True)


def main_recursive():
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            filename = os.path.join(root, file)
            if filename.endswith(".cdr"):
                #if filename doesnt include backup
                if "backup" not in filename.lower():
                    print(f'Generating outputs for {filename}')
                    oom_corel.generate_outputs(filename=filename, overwrite=False)




if __name__ == '__main__':
    main_recursive()