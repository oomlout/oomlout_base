import os
import oom_markdown

#find all the cdr files in the directory it was launched from and then run do_stuff(filename) to each one


def main(**kwargs):
    main_single_directory(kwargs)

def main_single_directory(kwargs):
    #find all cdr files in the directory it was launched from
    directory = kwargs.get("directory",os.getcwd())
    #directory = "C:\GH\oomlout_ibbc_breakout_board_holder_oobb_3_2"
    #directory = "C:\GH\oomlout_oomp_electronic_project_usb_switch"
    #directory = r"C:\GH\oomlout_oomp_electronic_device_aliexpress_amp_meter_10_amp_0_28_inch_display"
    if "teardown" in directory:
        oom_markdown.generate_readme_teardown(directory=directory)
    else:
        oom_markdown.generate_readme_project(directory=directory)
    


if __name__ == '__main__':
    kwargs = {}
    #kwargs["directory"] = "C:\GH\oomlout_storage_ikea_sockerbit_stadium_seating_configuration"
    main_single_directory(kwargs)