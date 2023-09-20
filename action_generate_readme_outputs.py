import os
import oom_markdown

#find all the cdr files in the directory it was launched from and then run do_stuff(filename) to each one

def main_single_directory():
    #find all cdr files in the directory it was launched from
    directory = os.getcwd()
    #directory = "C:\GH\oomlout_ibbc_breakout_board_holder_oobb_3_2"
    directory = "C:\GH\oomlout_oomp_electronic_project_usb_switch"
    oom_markdown.generate_readme_project(directory=directory)
    


if __name__ == '__main__':
    main_single_directory()