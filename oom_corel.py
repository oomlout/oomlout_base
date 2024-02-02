import oom_base as ob
import os
import copy

def generate_outputs(**kwargs):
    filename = kwargs.get('filename', None)
    #convert / to \\
    filename = filename.replace("/", "\\")
    #if filename doesn't have a : ion it make it absolute
    if ":" not in filename:
        filename = os.getcwd() + "\\" + filename
    overwrite = kwargs.get('overwrite', False)
    skip_template = kwargs.get('skip_template', False)
    if "template" in filename.lower() and skip_template:
        print(f"skipping template {filename} ")
        return

    full_filename_dxf = filename.replace(".cdr", ".dxf")
    full_filename_pdf = filename.replace(".cdr", ".pdf")
    full_filename_svg = filename.replace(".cdr", ".svg")
    full_filename_png = filename.replace(".cdr", ".png")

    #if any of the full filenames doesn't exist then
    print(f"Checking if {filename} needs to be generated\noverwrite: {overwrite}")
    if not os.path.isfile(full_filename_pdf) or not os.path.isfile(full_filename_svg) or not os.path.isfile(full_filename_png) or not os.path.isfile(full_filename_dxf) or overwrite:
        #open the file
        open_file(filename=filename)
        #save as dxf
        if not os.path.isfile(full_filename_dxf) or overwrite:
            print(f"Saving {filename} as dxf")
            save_as(filename=filename, save_as_type='dxf')
        #save as pdf
        if not os.path.isfile(full_filename_pdf) or overwrite:
            print(f"Saving {filename} as pdf")
            save_as(filename=filename, save_as_type='pdf')
        #save as svg
        if not os.path.isfile(full_filename_svg) or overwrite:
            print(f"Saving {filename} as svg")
            save_as(filename=filename, save_as_type='svg')
        #save as png
        if not os.path.isfile(full_filename_png) or overwrite:
            print(f"Saving {filename} as png")
            save_as(filename=filename, save_as_type='png')
        
        
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
    # issue with window getting unfocused so alt tab away then back
    ob.send_keys_alt_tab()
    ob.delay(2)
    ob.send_keys_alt_tab()            
    #send tab
    ob.send_tab()
    ob.delay(5)
    #send file type
    #send save_as type key by key
    for i in range(len(save_as_type)):
        ob.send_keys(save_as_type[i])
        ob.delay(0.2)    
    ob.delay(5)
    #send enter
    ob.send_enter()
    ob.delay(5)
    #swend shift tab once
    ob.send_tab_shift()
    ob.delay(10)
    #send filename
    ob.send_keys(filename)
    ob.delay(10)
    #send enter
    ob.send_enter()
    ob.delay(2)
    #send y
    ob.send_keys('y')
    ob.delay(10)
    #if save as type is pdf
    if save_as_type == 'pdf':
        ob.delay(10)
        ob.send_keys('y', dela=2) 
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

def dxf_to_cdr(**kwargs):
    kwargs["file_type"] = "dxf"
    import_to_cdr(**kwargs)

def svg_to_cdr(**kwargs):
    kwargs["file_type"] = "svg"
    import_to_cdr(**kwargs)

def import_to_cdr(**kwargs):
    file_type = kwargs.get('file_type', None)
    directory_base = "c:/gh/oomlout_base"
    file_template = f"{directory_base}/templates/blank.cdr"
    file_template = file_template.replace("/", "\\")
    filename = kwargs.get('filename', "")
    filename = filename.replace("/", "\\")
    p3 = copy.deepcopy(kwargs)
    
    p3["filename"] = file_template
    open_file(**p3)
    ob.delay(10)
    #send ctrl i
    ob.send_keys_ctrl('i', dela=5)
    ob.send_keys(filename, dela=2)
    ob.send_enter(dela=10)
    ob.send_enter(dela=10)
    ob.mouse_click(500,500, dela=5)
    ob.send_keys_ctrl('enter', dela=5)
    ob.send_tab(dela=1)
    ob.send_keys(300)
    ob.send_tab(dela=1)
    ob.send_keys(300)
    ob.send_enter(dela=2)
    #save as
    ob.send_keys_alt('f')
    ob.send_keys_down(times=6, dela=1)
    ob.send_enter(dela=10)
    filename = filename.replace(f".{file_type}", ".cdr")
    ob.send_keys(filename, dela=2)
    ob.send_enter(dela=2)
    ob.send_keys('y', dela=2)
    ob.send_keys_alt('f')
    ob.send_keys_up(times=1, dela=1)
    ob.send_enter(dela=5)










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


