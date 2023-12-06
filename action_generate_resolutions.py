import oom_base
import os

def main():
    directory = os.getcwd()
    oom_base.image_resolutions_dir(directory=directory, overwrite=False)



if __name__ == '__main__':
    main()