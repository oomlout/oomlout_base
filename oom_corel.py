import oom_base as ob
import os


def generate_outputs(**kwargs):
    filename = kwargs.get('filename', None)
    #convert / to \\
    filename = filename.replace("/", "\\")
    #if filename doesn't have a : ion it make it absolute
    if ":" not in filename:
        filename = os.getcwd() + "\\" + filename
    overwrite = kwargs.get('overwrite', False)

    full_filename_pdf = filename.replace(".cdr", ".pdf")
    full_filename_svg = filename.replace(".cdr", ".svg")
    full_filename_png = filename.replace(".cdr", ".png")
    full_filename_dxf = filename.replace(".cdr", ".dxf")

    #if any of the full filenames doesn't exist then
    if not os.path.isfile(full_filename_pdf) or not os.path.isfile(full_filename_svg) or not os.path.isfile(full_filename_png) or not os.path.isfile(full_filename_dxf) or overwrite:
        #open the file
        open_file(filename=filename)
        #save as pdf
        if not os.path.isfile(full_filename_pdf) or overwrite:
            save_as(filename=filename, save_as_type='pdf')
        #save as svg
        if not os.path.isfile(full_filename_svg) or overwrite:
            save_as(filename=filename, save_as_type='svg')
        #save as png
        if not os.path.isfile(full_filename_png) or overwrite:
            save_as(filename=filename, save_as_type='png')
        #save as dxf
        if not os.path.isfile(full_filename_dxf) or overwrite:
            save_as(filename=filename, save_as_type='dxf')
        
        close_file()

def save_as(filename, save_as_type='pdf',**kwargs):
    print(f"Saving {filename} as {save_as_type}")
    #if filename ends with .cdr change it to ending with save_as_type
    if filename.endswith(".cdr"):
        filename = filename.replace(".cdr", f".{save_as_type}")
    #send ctrl shift s
    ob.send_keys_alt('f')
    ob.delay(2)
    #if type is png
    if save_as_type == 'png':
        ob.send_keys('e')
    else:
        ob.send_keys('a')
    ob.delay(5)
    #send tab
    ob.send_tab()
    ob.delay(5)
    #send file type
    ob.send_keys(save_as_type)
    ob.delay(5)
    #send enter
    ob.send_enter()
    ob.delay(2)
    #swend shift tab once
    ob.send_tab_shift()
    ob.delay(2)
    #send filename
    ob.send_keys(filename)
    ob.delay(2)
    #send enter
    ob.send_enter()
    ob.delay(2)
    #send y
    ob.send_keys('y')
    ob.delay(10)
    #if save as type is pdf
    if save_as_type == 'pdf':
        pass
    #if save as type is svg
    if save_as_type == 'svg':
        #send escape
        ob.send_tab(dela=2)
    #if save as type is png
    if save_as_type == 'png':
        ob.delay(10)
        ob.send_keys('y', dela=2)        
        #send tab
        ob.send_tab(dela=2)
    #if save as type is dxf
    if save_as_type == 'dxf':
        pass
    ob.send_enter()
    ob.delay(10)
    ob.delay(2)


def open_file(**kwargs):
    filename = kwargs.get('filename', None)
    #open filename using os.system
    os.system(f"start {filename}")
    ob.delay(10)
    #save as pdf

def close_file():
    #send alt f
    ob.send_keys_alt('f')
    ob.delay(1)
    #send c
    ob.send_keys('c')
    ob.delay(5)


