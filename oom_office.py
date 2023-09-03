



def generate_outputs(**kwargs):
    calc_convert_ods_to_csv(**kwargs)
    #calc_convert_ods_to_png(**kwargs)


def calc_convert_ods_to_csv(**kwargs):
    filename = kwargs.get('filename', "")
    #use os.system to convert filename to csv on the command line
    import os
    #convert the ods file to csv
    os.system(f'soffice --headless --convert-to csv {filename}')

def calc_convert_ods_to_png(**kwargs):
    filename = kwargs.get('filename', "")
    #use os.system to convert filename to csv on the command line
    import os
    #convert the ods file to csv scale to fit all data
    os.system(f'soffice --headless --convert-to png --convert-options "Size=1000,FitToSize=1" {filename}')