



def generate_outputs(**kwargs):
    calc_convert_ods_to_csv(**kwargs)
    #calc_convert_ods_to_png(**kwargs)


def calc_convert_ods_to_csv(**kwargs):
    filename = kwargs.get('filename', "")
    #use os.system to convert filename to csv on the command line
    import os
    #convert the ods file to csv
    dir_out = os.path.dirname(filename)
    os.system(f'soffice --headless --convert-to csv --outdir {dir_out} {filename}')

def calc_convert_ods_to_png(**kwargs):
    filename = kwargs.get('filename', "")
    #use os.system to convert filename to csv on the command line
    import os
    #convert the ods file to csv scale to fit all data
    os.system(f'soffice --headless --convert-to png --convert-options "Size=1000,FitToSize=1" {filename}')

import os

def calc_convert_ods_to_xls(**kwargs):

    filename = kwargs.get('filename', "")
    #make filename absolute
    import os
    filename = os.path.abspath(filename)
    directory = os.path.dirname(filename)
    print(f"converting to xls {filename}")
    #use os.system to convert filename to csv on the command line
    import os
    #convert the ods file to csv scale to fit all data
    os.system(f'soffice --headless --convert-to xls:"MS Excel 97" --outdir {directory} {filename}')


def load_csv_to_dict(**kwargs):
    return_value = []
    filename = kwargs.get('filename', "")
    skip_rows = kwargs.get('skip_rows', 0)
    import csv
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i in range(skip_rows):
            next(reader)
        for row in reader:
            return_value.append(row)
    return return_value
    