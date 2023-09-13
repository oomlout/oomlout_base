
from oomBase import *
import os

from kiutils.board import Board
from kiutils.items.common import Position

def kicad_set_components(**kwargs):
    board_file = kwargs.get('board_file', None)
    board_file = board_file.replace('\\', '/')
    components = kwargs.get('components', None)   
    if components == None:
        components = kwargs.get('parts', None)   

    board = Board.from_file(board_file)
    footprints = board.footprints
    for component in components:
        for footprint in footprints:        
            #get reference by going through components.graphicItems until typw is 'reference' then make ref equal to text
            reference = None
            new_rotation = None
            for graphicItem in footprint.graphicItems:
                try:
                    if graphicItem.type == 'reference':
                        reference = graphicItem.text
                except:
                    pass
                    #skip lines and rectangles

            designator = component.get('designator', "")
            if designator == "":
                designator = component.get('reference', "")
            
            if designator == "":
                print(f"Error: No designator or reference for {component}")

            if reference.lower() == designator.lower():
                current_pos = footprint.position                
                current_angle = current_pos.angle
                if current_angle == None:
                    current_angle = 0
                new_pos = component.get('position', "")
                if new_pos == "":
                    position_x = component.get('position_x', "")
                    position_y = component.get('position_y', "")
                    rotation = component.get('rotation', None)
                    if rotation != None:
                        rotation = rotation
                        if rotation == "":
                            rotation = 0
                        new_rotation = float(rotation) - current_angle
                    else:
                        rotation = 0
                    
                    if position_x != "" and position_y != "":
                        new_pos = (position_x, position_y, rotation)
                    else:
                        new_pos = current_pos
                if new_pos != current_pos:
                    if len(new_pos) == 2:
                        new_pos = (new_pos[0], new_pos[1], 0)
                    corel_pos = component.get('corel_pos', True)
                    #if corel_pos isn't a boolean
                    if type(corel_pos) == str:
                        if corel_pos.lower() == "true":
                            corel_pos = True
                    if corel_pos:                       
                        corel_p = get_from_corel_coord(new_pos[0], new_pos[1]  )
                        new_pos = (corel_p[0], corel_p[1], new_pos[2])
                    new_pos = Position(new_pos[0], new_pos[1], new_pos[2])
                footprint.position = new_pos
                #### rotate pads if rotation is changed
                if new_rotation != None:
                    for pad in footprint.pads:
                        old_position = pad.position
                        old_angle = old_position.angle
                        if old_angle == None:
                            old_angle = 0
                        new_angle = old_angle + new_rotation
                        new_position = Position(old_position.X, old_position.Y, new_angle)
                        pad.position = new_position
                
    
    board.filePath = board.filePath.replace('.kicad_pcb', '_new.kicad_pcb')
    print(f"Saving {board.filePath}")
    board.to_file()

def get_from_corel_coord(x,y):
    x = float(x)
    y = -float(y)
    return (x,y)


def generate_outputs(**kwargs):   
    return_value = 0 
    define_mouse_positions(**kwargs)
    return_value += generate_outputs_board(**kwargs)
    return_value += generate_outputs_schematic(**kwargs)
    if return_value > 0:
        return_value = 1
    return return_value

def generate_outputs_board(**kwargs):
    return_value = 0
    #get current working directory as a string
    import os
    current_working_directory = os.getcwd().replace("\\","/")

    filename = kwargs.get('filename', None)
    basename = os.path.basename(filename)
    #remove extension
    basename = basename.split(".")[0]
    if filename == None:
        board_file = kwargs.get('board_file', rf"{current_working_directory}\oomp\current_version\working\working.kicad_pcb")
    else:
        board_file = filename
    #if board file doesn't start with a drive
    if not board_file[1] == ":":
        board_file = rf"{current_working_directory}/{board_file}"
    kicadBoard = board_file
    #replace // with /
    kicadBoard = kicadBoard.replace("//","/")

    overwrite = kwargs.get('overwrite', True)
    #get the directory of board_file and set dir to be it
    dir = os.path.dirname(board_file) + "/"
    #replace backslashes with slashes
    dir = dir.replace("\\","/")
    print("Harvesting Kicad Board File: " + kicadBoard)
    #test if the last 3d render exists if it does skip the rest
    if not os.path.isfile(dir + f"{basename}_3d.png") or overwrite:
        oomLaunchPopen("pcbnew.exe " + kicadBoard,15)
        #deal with already open error
        #send right
        oomSendRight(delay=2)
        #send enter
        oomSendEnter(delay=2)
        oomSendEnter(delay = 5)
        oomMouseMove(pos=kicadFootprintMiddle,delay=2)
        oomSend("b",10)
        oomMouseClick(pos=kicadActive,delay=5)  
        
        filename = dir
        filename = filename.replace("\\","/") 
        filename = filename.replace("//","/")
        oomMakeDir(filename)      
        kicad_export_interactive_bom(filename=filename,overwrite=overwrite, basename=basename)


        kicadExport(filename,"pdf",overwrite=overwrite, basename=basename)
        kicadExport(filename,"bom",overwrite=overwrite, basename=basename)
        kicadExport(filename,"pos",overwrite=overwrite, basename=basename)                
        kicadExport(filename,"svg",overwrite=overwrite, basename=basename)            
        #kicadExport(filename,"wrl",overwrite=overwrite)
        #kicadExport(filename,"step",overwrite=overwrite)
        kicadExport(filename,"3dRender",overwrite=overwrite, basename=basename)
        kicadClosePcb()    
    return return_value 

def kicad_export_interactive_bom(**kwargs):
    filename = kwargs.get('filename', None)
    basename = kwargs.get('basename', "working")
    overwrite = kwargs.get('overwrite', False)        
    #send alt t
    oomSendAltKey("t",delay=2)
    # send e
    oomSend("e",delay=2)
    # send g
    oomSend("g",delay=2)

    # turn off open browser and compression
    #send right
    oomSendRight(delay=2)
    #send shift tabe 4 tinmes
    oomSendShiftTab(times=4,delay=2)
    #send space
    oomSendSpace()
    #delay 2
    oomDelay(2)
    #send shift tab
    oomSendShiftTab(delay=2)
    #send space
    oomSendSpace()
    #delay 2
    oomDelay(2)
    # send enter


    oomSendEnter(delay=10)


def generate_outputs_schematic(**kwargs):   
    return_value = 0
    overwrite = kwargs.get('overwrite', False)
    #get current working directory as a string
    import os
    current_working_directory = os.getcwd()     
    board_file = kwargs.get('board_file', "none")
    if board_file == "none":
        board_file = kwargs.get('filename', rf"{current_working_directory}\oomp\current\working\working.kicad_pcb")
    #change to sch file
    board_file = board_file.replace(".kicad_pcb",".kicad_sch")
    basename = os.path.basename(board_file)
    #remove extension
    basename = basename.split(".")[0]
    #if board file doesn't start with a drive
    if not board_file[1] == ":":
        board_file = rf"{current_working_directory}\{board_file}"

    kicadBoard = board_file
    directory = os.path.dirname(board_file) + "/"
    imageFile = directory + f"{basename}_schematic.png"
    pdfFile = directory + f"{basename}_schematic.pdf"
    if os.path.isfile(kicadBoard):
        if overwrite or not os.path.isfile(imageFile):
            print("Harvesting Kicad Board File: " + kicadBoard)
            return_value = 1
            oomLaunchPopen("eeschema.exe " + kicadBoard,10)
            ###### check if its an error
            oomSetClipboard("")
            oomDelay(1)
            oomCopy()
            oomDelay(2)
            check_error = oomGetClipboard()
            if "KiCad PCB Editor Error" in check_error:
                oomSendEnter()
                oomDelay(2)                   
                kicadClosePcb()         
                #make a new file text file with name imageFile
                #f = open(imageFile, "w")
                #f.write("Error")
                #f.close()
 
                return 

            oomSendEnter()
            oomDelay(2)   
            #deal with already open error
            #send right
            oomSendRight(delay=2)
            #send enter
            oomSendEnter(delay=2)
            #send enter
            oomSendEnter(delay=2)
            #maximize
            #oomSendMaximize()
            #zoom to schematic rather than page
            oomSendControl("home",delay=2)
            oomDelay(2)
            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomMouseMove(pos=kicadActive,delay=2)
            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomMouseMove(pos=kicadActive,delay=2)
            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomMouseMove(pos=kicadActive,delay=2)
            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomMouseClick(pos=kicadActive,delay=5)    
            
            # bom
            #send alt t
            oomSendAltKey("t",delay=2)
            #send up twice
            oomSendUp(times=2,delay=2)
            #send enter
            oomSendEnter(delay=2)
            #select filter press down three times
            oomSendDown(times=3,delay=2)
            #send tab four times
            oomSendTab(times=3,delay=2)
            #send paramter string
            string_parameter = 'python "C:/Program Files/KiCad/7.0/bin/scripting/plugins/bom_csv_grouped_by_value_with_fp.py" "{%}I" "{%}O_bom_schematic.csv'
            oomSend(string_parameter,delay=2)
            #send one tab
            oomSendTab(delay=2)
            #send enter
            oomSendEnter(delay=2)
            #send esc
            oomSendEsc(delay=2)




            # image
            #oomSendAltKey("f",delay=2)            
            oomMouseClick(pos=kicadFile,delay=5)   
            oomSend("e",1)
            oomSendEnter(delay=2)
            oomClipboardSaveImage(imageFile)

            ###### plot pdf
            oomMouseClick(pos=kicadFile,delay=5)
            oomSend("ppp",2)
            oomSendEnter(delay=2)
            #'send temp dir
            tempDir = 'tmp/'    
            oomSend(tempDir.replace("/","\\"),2)
            oomSendEnter(delay=2)
            #move and rename file
            src = f'{directory}tmp/{basename}.pdf'
            dest = f'{directory}{basename}_schematic.pdf'
            #delete if the dest exists
            if os.path.isfile(dest):
                os.remove(dest)
            if os.path.isfile(src):
                try:
                    os.rename(src, dest)
                except Exception as e:
                    print(f"Error renaming {src} to {dest} probbly missing src")
                    print(e)
            #delete the tmp directory and files in it
            temp_directory = f'{directory}{tempDir}'
            #if the directory exists
            if os.path.exists(temp_directory):
                shutil.rmtree(f'{directory}{tempDir}')
            #send esc
            oomSendEsc(delay=2)
            oomSendEsc(delay=2)
            oomSendEsc(delay=2)




            kicadClosePcb()
            oomSendEsc(delay=5)
    return return_value

def generate_outputs_symbol(**kwargs):
    counter = 0
    current_working_directory = os.getcwd().replace("\\","/")

    filename = kwargs['filename']
    #if filename doesn't have 
    if not filename[1] == ":":
        filename = rf"{current_working_directory}/{filename}"
    #//make \\ /
    filename = filename.replace("\\","/")

    overwrite = kwargs.get('overwrite', False)

    kicadBoard = filename
    symbol_name = filename.split("/")[-3].replace(".kicad_sym","")
    pngFileName = filename.replace(".kicad_sym",".png")
    svgFileName = filename.replace(".kicad_sym",".svg")
    symbolFileName = filename
    print("Harvesting Kicad Symbol File: " + filename)
    if overwrite or not os.path.isfile(svgFileName) or not os.path.isfile(pngFileName) or not os.path.isfile(symbolFileName):
        print("    Generating")
        oomMouseClick(pos=kicadActive, delay=5)        
        oomMouseClick(pos=kicadFootprintFilter, delay=5)
        oomSendCtrl("a")
        oomDelay(1)
        oomSendDelete(delay=1)
        oomSend(symbol_name,delay=2)

        oomSendEnter(delay=3)
        oomMouseClick(pos=kicadFootprintFirstResult, delay=0.1)
        oomMouseClick(pos=kicadFootprintFirstResult, delay=5)
        oomMouseClick(pos=kicadFootprintFirstResult, delay=10)

        #check if png exists
        if not os.path.isfile(pngFileName):
            exportKicadSymbol(pngFileName,"png")
        if not os.path.isfile(svgFileName):
            exportKicadSymbol(svgFileName,"svg")
        if not os.path.isfile(symbolFileName):
            exportKicadSymbol(symbolFileName,"kicad_sym")
        oomDelay(5)
        counter = 1
    return counter

def exportKicadSymbol(filename,type):
    oomMouseClick(pos=kicadFootprintFirstResult, delay=5)    
    oomSendAltKey("f",delay=2)
    oomSend("e",delay=2)
    down = 0
    if type == "png":
        down = 1
    if type == "svg":
        down = 2
    oomSendDown(times=down,delay=2)
    oomSendEnter(delay=2)
    oomSend(filename.replace("/","\\"), delay=2)
    oomSendEnter(delay=2)
    if type == "kicad_sym":
        oomSendEnter(delay=2)

    oomSend("y",delay=2)
    oomSendEnter(delay=2)
    if type == "kicad_sym":
        oomSendEnter(delay=2)

def generate_outputs_footprint(**kwargs):
    counter = 0
    computer = kwargs.get("computer","desktop")
    define_mouse_positions(computer=computer)
    filename = kwargs.get('filename', None)
    #replace \\ with /
    filename = filename.replace("\\","/")
    #get directory from filename
    directory = os.path.dirname(filename) + ""
    #if no drive letter add current working directory
    if not filename[1] == ":":
        directory = os.getcwd() + "/" + directory
    #replace \\ with /
    directory = directory.replace("\\","/")
    
    overwrite = kwargs.get('overwrite', False)
    #load footprint details from directoery working.yaml
    import yaml
    footprint = yaml.load(open(directory + "/working.yaml"), Loader=yaml.FullLoader)

    
    oompFileName = f'{directory}/working.png'
    oompFileName3D = f'{directory}/working_kicad_pcb_3d.png'
    oompFileName3Dfront = f'{directory}/working_kicad_pcb_3d_front.png'
    oompFileName3Dback = f'{directory}/working_kicad_pcb_3d_back.png'
    oomp_filename_pdf = f'{directory}/working.pdf'
    footprintFilename = f'{directory}/working.kicad_mod'
    #last directory in filename is footprint fullname
    footprint_fullname = filename.split("/")[-3]
    

    #if overwrite or not os.path.isfile(oompFileName) :
    if overwrite or not os.path.isfile(oompFileName3D) :
        print("    Harvesting files")
        shortDelay = 1
        longDelay = 3
        footprintName = footprint[0]["name"]
        footprintDir = footprint[0]["name"]
        print("Capturing :" + str(footprint))
        oomMouseClick(pos=kicadActive)
        oomDelay(shortDelay)
        ##apply filter
        oomMouseClick(pos=kicadFootprintFilter)
        oomDelay(shortDelay)
        oomSendCtrl("a")
        oomDelay(shortDelay)
        oomSend(footprint_fullname)
        oomDelay(longDelay)
        oomMouseDoubleClick(pos=kicadFootprintFirstResult)
        oomDelay(longDelay)
        #### Discard Changes
        oomSendRight()
        oomDelay(shortDelay)
        oomSendEnter()
        oomDelay(longDelay)
        #print to pdf
        oomSendAltKey("f",5)
        oomSend("p",5)
        oomSendEnter(delay=2)
        oomSendEnter(delay=2)
        oomSend(oomp_filename_pdf.replace("/","\\"),delay=2)
        oomSendEnter(delay=2)
        oomSend("y",2)
        #wait 10 seconds
        oomDelay(10)
        oomSendEsc(delay=5)
        #### Export PNG
        file = oompFileName.replace("/","\\")
        if not os.path.exists(file):
            oomSendAltKey("f",2)
            oomSend("e",1)
            oomSend("p",2)
            oomSend(file,3)
            oomSendEnter(delay=1)
            oomSend("y",2)
        #### Export Footprint
        oomMouseClick(pos=kicadFootprintFilter)
        file = footprintFilename.replace("/","\\")
        if not os.path.exists(file):        
            oomSendAltKey("f",2)
            oomSend("e",1)
            oomSend("f",2)
            oomSend(file,3)
            oomSendEnter(delay=1)
            oomSend("y",2)
            oomSendEnter(delay=1)
        #### 3d 
        oomMouseClick(pos=kicadFootprintView,delay=1)
        oomSendDown(times=2,delay=1)
        oomSendEnter(delay=5)
        #oomSendWindowsKey("up")
        ##### raytracing
        #if "_BALL" not in oompID.upper() and "_FLG" not in oompID.upper():
        #    oomSendAltKey("p",1)
        #    oomSendEnter(2)
        #    oomDelay(10)
        #### front
        oomSendAltKey("f",2)
        oomSendEnter(delay=1)
        oomSend(oompFileName3Dfront.replace("/","\\"),3)
        oomSendEnter(delay=1)
        oomSend("y",2)
        oomMouseClick(pos=[595,60],delay=5)
        oomMouseClick(pos=[818,536],delay=5) ###### click middle
        oomSend("Z",2)       
        #### back        
        oomDelay(10)
        oomSendAltKey("f",2)
        oomSendEnter(delay=1)
        oomSend(oompFileName3Dback.replace("/","\\"),3)
        oomSendEnter(delay=1)
        oomSend("y",2)  
        oomMouseClick(pos=[818,536],delay=5) ###### click middle
        oomSend("r",2)       
        #### ortho
        #oomMouseClick(pos=[595,60],delay=5)  
        # Needs hotkey setting rotate x clockwise to a, z counter clockwise to d 
        #yaxis
        times = 3
        for x in range(times):
            oomMouseClick(pos=kicad3dView,delay=1)
            oomSend("rr")
            oomSendEnter(delay=1)
        #zaxis    
        times = 2
        for x in range(times):
            oomMouseClick(pos=kicad3dView,delay=1)
            oomSend("rrrrrrr")
            oomSendEnter(delay=1)
        oomMouseClick(pos=[818,536],delay=5) ###### click middle
        oomSendAltKey("f",2)
        oomSendEnter(delay=1)
        oomSend(oompFileName3D.replace("/","\\"),3)
        oomSendEnter(delay=1)
        oomSend("y",2)
        oomMouseClick(pos=[818,536],delay=5) ###### click middle
        



        ##### close
        oomSendAltKey("f",delay=1)
        oomSendUp(delay=1)
        oomSendEnter(delay=3)







        oomDelay(longDelay)    

        oomDelay(5)
        counter = 1
    return counter


kicadActive =[515,14]
kicadFile = [80,35]
kicadFootprintMiddle = [945,545] 
kicad3dView = [145,35]
kicadActive =[515,14]
kicadFootprintFilter =[145,114]
kicadFootprintFirstResult = [145,185]
kicadFootprintMiddle = [945,545] 
kicadFootprintMiddlePlus = [950,550] 
kicadFootprintTopLeft = [365,86] 
kicadSymbolMiddle = [1105,555] 
kicadSymbolMiddlePlus = [1110,560] 
kicadFootprintView = [153,36]

kicadFile = [80,35]
kicad3dView = [145,35]

def define_mouse_positions(**kwargs):

    computer = kwargs.get("computer","desktop")
    global kicadFile, kicadActive, kicadFile, kicadFootprintMiddle, kicad3dView, kicadActive, kicadFootprintFilter, kicadFootprintFirstResult, kicadFootprintMiddle, kicadFootprintMiddlePlus, kicadFootprintTopLeft, kicadSymbolMiddle,kicadSymbolMiddlePlus, kicadFootprintView

    if computer == "desktop":
        kicadFile = [80,35]
        kicadActive =[515,14]
        kicadFile = [80,35]
        kicadFootprintMiddle = [945,545] 
        kicad3dView = [145,35]
        kicadActive =[515,14]
        kicadFootprintFilter =[145,114]
        kicadFootprintFirstResult = [145,185]
        kicadFootprintMiddle = [945,545] 
        kicadFootprintMiddlePlus = [950,550] 
        kicadFootprintTopLeft = [365,86] 
        kicadSymbolMiddle = [1105,555] 
        kicadSymbolMiddlePlus = [1110,560] 
        kicadFootprintView = [153,36]
    elif computer == "surface":        
        kicadFile = [19,50]
        kicadFootprintMiddle = [945,545] 
        kicad3dView = [145,35]
        kicadActive =[515,14]
        kicadFootprintFilter =[145,169] ####
        kicadFootprintFirstResult = [86,270] ####
        kicadFootprintMiddle = [945,545] 
        kicadFootprintMiddlePlus = [950,550] 
        kicadFootprintTopLeft = [365,186] 
        kicadSymbolMiddle = [1105,555] 
        kicadSymbolMiddlePlus = [1110,560] 
        kicadFootprintView = [131,52]


def kicadExport(filename,type,overwrite=False, **kwargs):
    basename = kwargs.get('basename', "working")
    #remove extension
    basename = basename.split(".")[0]
    if type.lower() == "bom":        
        bomFile = filename + f"{basename}_bom.csv"
        if overwrite or not os.path.isfile(bomFile):
            print("    Making bom file")
            #oomSendAltKey("f",2)
            oomMouseClick(pos=kicadFile,delay=5)       
            oomSend("f",2)
            oomSend("b",2)
            oomSend(bomFile.replace("/","\\"),5)
            oomSendEnter(2)
            oomSend("y",2)
    if type.lower() == "pos":
        bomFile = filename + f"{basename}.pos"
        if overwrite or not os.path.isfile(bomFile):
            print("    Making bom file")
            #oomSendAltKey("f",2)
            oomMouseClick(pos=kicadFile,delay=5)       
            oomSend("f",2)
            oomSend("c",2)
            oomSend(filename.replace("/","\\"),5)
            oomSendShiftTab(2)
            oomSendEnter(2)   
            oomSendEsc(2)         
    if type.lower() == "svg":
        if overwrite or not os.path.isfile(filename + f"{basename}.svg"):
            print("    Making svg files")
            #oomSendAltKey("f",2)
            oomMouseClick(pos=kicadFile,delay=5)       
            oomSend("e",2)
            oomSend("ss",2)
            oomSendEnter(delay=2)
            oomSend(filename,5)
            oomSendShiftTab(2,delay=2)
            oomSendEnter(delay=10)
            oomSendEsc(5)
            #rename the file
            src = f'{filename}{basename}-brd.svg'
            dst = f'{filename}{basename}.svg'
            #if dst exists delete it
            if os.path.isfile(dst):
                os.remove(dst)
            try:
                os.rename(src, dst)
            except:
                print(f"Error renaming {src} to {dst} probbly missing src")
    if type.lower() == "pdf":
        if overwrite or not os.path.isfile(filename + f"{basename}.pdf"):
            print("    Making pdf files")
            #oomSendAltKey("f",2)
            oomMouseClick(pos=kicadFile,delay=10)       
            oomSend("pp",2)            
            oomSendEnter(delay=10)
            oomSendEnter(delay=10)
            oomSendEnter(delay=10)
            file_pdf = f"{filename}{basename}.pdf"
            #replace / with \\
            file_pdf = file_pdf.replace("/","\\")
            oomSend(file_pdf,5)
            oomSendEnter(delay=5)
            oomSend("y",15)
            oomSendEsc(5)
    if type.lower() == "wrl":
        if overwrite or not os.path.isfile(filename + f"{basename}.wrl"):
            print("    Making wrl file")
            oomMouseClick(pos=kicadFile,delay=5)       
            oomSend("e",2)
            oomSend("v",5)
            oomSendShiftTab(2,delay=2)
            oomSendEnter(delay=2)
            oomSend("y",8)
            oomSendEsc(5)
    if type.lower() == "step":
        if overwrite or not os.path.isfile(filename + f"{basename}.step"):
            print("    Making step file")
            oomMouseClick(pos=kicadFile,delay=5)       
            oomSend("e",2)
            oomSend("s",5)
            oomSendEnter(delay=2)
            oomSendShiftTab(4,delay=2)
            oomSendEnter(delay=10)
            oomSendAltKey('f4',5)
            oomSendEsc(5)
    if type.lower() == "3drender":
        if overwrite or not os.path.isfile(filename + f"{basename}_3d.png"):
            filename = filename.replace("\\\\","\\")
            filename = filename.replace("//","/")
            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomSendAltKey("3",5)
            ###### zoom
            oomMouseClick(pos=kicad3dView,delay=1)
            oomSend("z")
            oomSendEnter(delay=1)
            ######  front
            currentFile = filename + f"{basename}_3d_front.png"
            oomMouseClick(pos=kicadFile,delay=5) 
            oomSend("e",2)
            oomSendEnter(delay=2)
            oomSend(currentFile.replace("/","\\"),2)
            oomSendEnter(delay=2)
            oomSend("y",2)
            ######  back
            currentFile = filename + f"{basename}_3d_back.png"
            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomMouseRight(1)
            oomSend("vv",0.5)
            oomSendEnter(2)

            
            ###### zoom
            oomMouseClick(pos=kicad3dView,delay=1)
            oomSend("z")
            oomSendEnter(delay=1)
            oomMouseClick(pos=kicadFile,delay=5) 
            oomSend("e",2)
            oomSendEnter(delay=2)
            oomSend(currentFile.replace("/","\\"),2)
            oomSendEnter(delay=2)
            oomSend("y",2)
            ######  ortho
            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomMouseRight(1)
            oomSend("v",0.5)
            oomSendEnter(2)
            ###### zoom
            oomMouseClick(pos=kicad3dView,delay=1)
            oomSend("z")
            oomSendEnter(delay=1)            
            #yaxis
            times = 3
            for x in range(times):
                oomMouseClick(pos=kicad3dView,delay=1)
                oomSend("rr")
                oomSendEnter(delay=1)
            #zaxis    
            times = 2
            for x in range(times):
                oomMouseClick(pos=kicad3dView,delay=1)
                oomSend("rrrrrrr")
                oomSendEnter(delay=1)

            currentFile = filename + f"{basename}_3d.png"
            oomMouseClick(pos=kicadFile,delay=5) 
            oomSend("e",2)
            oomSendEnter(delay=2)
            oomSend(currentFile.replace("/","\\"),2)
            oomSendEnter(delay=2)
            oomSend("y",2)
            ###### close
            oomMouseClick(pos=kicadFile,delay=5) 
            oomSend("c",2)

def open_footprint_window():
    #open kicad.exe and wait 10 seconds
    oomLaunchPopen("kicad.exe",10)
    #maximize
    oomSendMaximize()
    #click at 400,240 opwen footpritn editor
    oomMouseClick(pos=[400,260],delay=5)
    #send enter
    oomSendEnter(delay=5)
    #maximize
    oomSendMaximize()
    #wait for footprints to load 10 seconds
    oomDelay(10)
    #press enter
    oomSendEnter(delay=5)


def kicadClosePcb(noSave=True,eda=False):
    #oomSendAltKey("f",2)
    oomMouseClick(pos=kicadFile,delay=5)
    oomSendUp(delay=2)
    oomSendEnter(delay=2)
    if noSave:
        oomSendRight(delay=2)
    if eda:
        oomSendEnter(delay=5)
    else:
        oomSendEnter(delay=20)

def eagle_to_kicad(**kwargs):
    computer = kwargs.get("computer","desktop")
    define_mouse_positions(computer=computer)
    #get the working directory
    import os
    current_working_directory = os.getcwd()
    #replace backslashes with slashes
    current_working_directory = current_working_directory.replace("\\","/")
    eagle_file = kwargs.get('eagle_file', None)
    if eagle_file == None:
        eagle_file = kwargs.get("filename", rf"{current_working_directory}\oomp\current\working\working.brd")
    #get ther directory from eagle_file
    eagle_directory = os.path.dirname(eagle_file)
    kicad_directory = eagle_directory
    overwrite = kwargs.get('overwrite', False)

    filename = f'{current_working_directory}/{eagle_file}'
    #remove any double slashe with single slashes
    filename = filename.replace("//","/")
    dir = f'{current_working_directory}/{kicad_directory}/'
    dir = dir.replace("\\","/")
    #remove any double slashe with single slashes
    dir = dir.replace("//","/")
    style = ""
    kicadBoard = dir + "working.kicad_pcb"
    kicad_board_file = kicadBoard
    kicad_schematic = dir + "working.kicad_sch"
    kicad_footprint_directory = dir + "working.pretty"

    
    boardEagle = filename
    #remove any double
    
    
    #if (overwrite or not os.path.exists(kicadBoard)) and os.path.exists(boardEagle):
    if (overwrite or not os.path.exists(kicad_board_file)) and os.path.exists(boardEagle):
        print(    "HarvestEagleBoardToKicad: " + filename)
        oomLaunchKicad()
        oomDelay(10)
        oomMouseClick(pos=kicadActive,delay=5)       
        oomMouseClick(pos=kicadFile,delay=5)       
        oomSendDown(8,delay=2)
        oomSendRight(1,delay=2)
        oomSendDown(1,delay=2)
        oomSendEnter(delay=5)
        ###### filedialog box open
        
        filename = boardEagle.replace("/","\\")
        oomSend(filename,5)
        oomSendEnter(10)
        ######  set temp folder
        tempDir = f'{current_working_directory}/tmp/eagle_to_kicad/'
        #create tmp directory if it doesn't exist
        if not os.path.exists(tempDir):
            os.makedirs(tempDir)
        #delete tempDir + "boardEagle.pretty/" if it exists using os
        # delete contents of temp_dir
        try:
            shutil.rmtree(tempDir)
        except:
            print("couldn't remove temp folder")
        # make temp_dir
        if not os.path.exists(tempDir):
            os.makedirs(tempDir)

        oomSend(tempDir.replace("/","\\"),2)
        oomSendEnter(5)        
        oomSendEnter(10)
        oomSend("y",10)
        #move to the right if theres a schemativc already open error
        oomSendRight(1,2)
        #check what the error is
        # clear clipboard
        oomSetClipboard("")
        #send ctrl c
        oomSendCtrl("a")
        oomDelay(2)
        oomSendCtrl("c")
        oomDelay(2)
        #get clipboard
        clipboard = oomGetClipboard()
        #if it is a schematic already open error
        
        if "Unable to read file" in clipboard:
            print(f"old eagle format converting")
            #convert in eagle
            #open filename in eagle with os.sysytem
            filenames = []
            filenames.append(filename)
            filenames.append(filename.replace(".brd",".sch"))
            for filename in filenames:
                #open filename in eagle with subprocess not os.system
                subprocess.Popen(["eagle", filename])
                #wait 10 seconds
                oomDelay(20)
                #maximize window
                #oomSendMaximize()
                #click on file button
                oomMouseClick(pos=kicadFile,delay=2)
                #down 1 time
                oomSendDown(4,delay=2)
                #enter
                
                oomSendEnter()
                oomDelay(2)
                oomSendEnter()
                oomDelay(2)
                oomSendEnter()
                oomDelay(2)
                #close
                #click on file button
                oomMouseClick(pos=kicadFile,delay=2)
                #send up once
                oomSendUp(1,delay=2)
                #enter
                oomSendEnter()
                oomDelay(5)
                oomSendEnter()
                oomDelay(5)
                oomSendEnter()
                oomDelay(5)
                oomSendEnter()
                oomDelay(5)
                oomSendEnter()
                oomDelay(5)
                kicadClosePcb(False)
                oomDelay(5)
                kicadClosePcb(False)
                oomDelay(10)
                return
            


        #cleaer badly formed xml error        
        oomSendEnter(10)
        oomSendEnter(10)
        oomSendEnter(5)
        #reset layer matching
        #send four tabs
        oomSendTab(4,2)
        #send enter
        oomSendEnter(2)
        ######  match layers dialog
        oomSendTab(6-4,5)
        oomSendEnter(2)
        oomSendTab(1,2)
        oomSendEnter(10)
        oomSendEsc(10)
        oomSendEsc(10)
        oomSendEsc(2)
        oomDelay(15)
        oomMouseClick(pos=kicadFootprintMiddle,delay=2)
        oomSendEsc(delay=2)
        #fill zones
        oomSend("b",30)
        ######  save board
        oomMouseClick(pos=kicadFile,delay=5)
        oomSendDown(3,delay=2)
        oomSendEnter(delay=5)
        oomSend(kicadBoard.replace("/","\\").replace("\\\\","\\"),2)
        oomSendEnter(delay=10)
        oomSend("y",2)
        oomSendEnter(delay=2)
        ###### close project
        kicadClosePcb(False)
        ###### save schematic
        filename_schematic = filename.replace(".brd",".sch")
        #if filename exists
        if os.path.isfile(filename_schematic):
                
            #test if it is multi sheet
            oomMouseClick(pos=kicadFootprintMiddle,delay=10)
            oomDelay(2)
            #clear clipboard
            oomSetClipboard("") 
            #send ctrl c
            oomSendCtrl("a")
            oomDelay(2)
            oomSendCtrl("c")
            oomDelay(2)
            #get clipboard
            clipboard = oomGetClipboard()
            last_clipboard = clipboard
            mouse_points_sheet = []
            mouse_points_sheet.append([160,110])
            #if it is multi sheet
            if "working_1.kicad_sch" in clipboard:
                print("multi sheet")           
                mouse_points_sheet.append([160,130])
                mouse_points_sheet.append([160,150])
                mouse_points_sheet.append([160,170])
                mouse_points_sheet.append([160,190])            
                mouse_points_sheet.append([160,210])
                #copy old to kicad_sch_old
                import shutil
                #shutil.copyfile(kicad_schematic, kicad_schematic.replace(".sch",".sch_old"))
            sheets = len(mouse_points_sheet)
            
            for x in range(0,sheets):
                print("sheet: " + str(x))
                oomMouseClick(pos=mouse_points_sheet[x],delay=5)    
                oomMouseClick(pos=kicadFootprintMiddle,delay=2)                
                oomSetClipboard("") 
                #send ctrl c
                oomSendCtrl("a")
                oomDelay(2)
                oomSendCtrl("c")
                oomDelay(2)
                #get clipboard
                clipboard = oomGetClipboard()
                if "working_1.kicad_sch" in clipboard and x != 0:
                    print("no more sheets")
                    break
                

                oomMouseClick(pos=kicadFile,delay=5)
                oomSendDown(2,delay=2)
                oomSendEnter(delay=5)
                filename2 = kicad_schematic.replace("/","\\").replace("\\\\","\\")
                if x > 0:
                    filename2 = filename2.replace("working.kicad_sch",f"working_{x}.kicad_sch")
                print(f"filename2: {filename2}")
                oomSend(filename2,2)


                oomSendEnter(delay=10)
                oomSend("y",2)
                oomSendEnter(delay=5)


        ###### close project
        kicadClosePcb(False)
        #copy footprint folder across
        #find the folder that ends .pretty in tmp
        tmpDir = f'tmp/'
        for file in os.listdir(tmpDir):
            if file.endswith(".pretty"):
                shutil.copytree(tmpDir+file, kicad_footprint_directory)

        
        
    else:
        pass
        print("skipping: " + filename + " already exists")

        

def generate_readme_old(**kwargs):
    import oomp
    oomp.load_parts(make_files=False)
    name = kwargs.get('name', None)
    description = kwargs.get('description', None)
    directory = kwargs.get('directory', "")
    oomp_in_output = kwargs.get('oomp_in_output', False)

    # time to make a readme for the provided project
    readme = f"# {name}\n"
    # if the file oomp/version_current/working/working_3d.png exists add it
    extra = "oomp_documentation/"
    if oomp_in_output:
        extra = ""
    if os.path.isfile(f"{directory}/oomp_documentation/version_current/working/working_3d.png"):
        readme += f"![{name}]({extra}version_current/working/working_3d.png)\n"
    # add description with header 
    
    readme += f"## Description\n"
    readme += f"{description}/\n"
    
    #add the schematic if it exists
    if os.path.isfile(f"{directory}/oomp_documentation/version_current/working/working_schematic.png"):
        readme += f"## Schematic\n"
        readme += f"![{name}]({extra}version_current/working/working_schematic.png)\n"
    
    # add the bom if it exists
    if os.path.isfile(f"{directory}/oomp_documentation/version_current/working/working_bom.csv"):
        readme += f"## Bill of Materials\n"
        #take the bom csv and import it as a dict using csv library don't add it to bom do it in one line rather than using a csvfile object it is seperated with ;
        bom = csv.DictReader(open(f"{directory}/oomp_documentation/version_current/working/working_bom.csv"), delimiter=';')
        #add the bom to the readme as a table
        #get the headers from the dict
        headers = bom.fieldnames
        #add the headers to the readme
        readme += f"| {' | '.join(headers)} |\n"
        #add the seperator
        readme += f"| {' | '.join(['---' for x in headers])} |\n"
        
        
        for row in bom:
            oomp_id  = ""
            try:
                oomp_id = row['Footprint']
                #remove everything before the the second underscore and the underscore
                oomp_id = oomp_id.split("_", 2)[2]
            except:
                pass
            if oomp_id in oomp.parts:
                #add an oomp item
                #create an empty string to make for the row
                row_string = ""
                #go through the headers
                for header in headers:
                    if header != "Designation":
                        value = row[header]         
                        #linewrap the value with a max line width of 20
                        value = "<br>".join([value[i:i+20] for i in range(0, len(value), 20)])
                        readme += f"| {value} "
                    else:
                        part = oomp.parts[oomp_id]
                        link = f"https://github.com/oomlout/oomlout_oomp_v3/tree/main/parts/{oomp_id}"
                        name = part.get("short_name", part.get("name", """no name"""))
                        readme += f"| [{name}]({link})<br>{part['short_code']}<br>{part['md5_6']} "
                        pass
            else:
                #add the row to the readme get the column names from the headers
                pass
                for header in headers:                 
                    value = row[header]         
                    #linewrap the value with a max line width of 20
                    value = "<br>".join([value[i:i+20] for i in range(0, len(value), 20)])
                    readme += f"| {value} "
                
            readme += f"|\n"
    # add extra images in the base directory and in the oomp/current directory check go through the directory to find them
    readme += f"\n## Images\n"
    #find all the pngs in the base directory and oomp/current
    pngs = []
    extra = ""
    if oomp_in_output:
        extra = "oomp_documentation/"
    for root, dirs, files in os.walk(f"{directory}{extra}"):
        for file in files:
            if file.endswith(".png") and "src/" not in root:
                pngs.append(os.path.join(root, file))   
    #add them to the readme
    for png in pngs:
        #add each png as a lnked image
        png = png.replace(directory, "")
        # remove extra
        png = png.replace(extra, "")
        png = png.replace(".\\", "")
        png = png.replace("\\", "/")
                          
        readme += f"![{png}]({png})\n"
        
    #write the readme
    extra = ""
    if oomp_in_output:
        extra = "oomp_documentation/"
    with open(f'{directory}{extra}readme.md', "w") as f:
        f.write(readme)
    

def copy_kibom_template(**kwargs):
    filename = kwargs.get('filename', None)
    template_file = kwargs.get('tamplate_file', 'templates/kibot_template.yaml')
    
    filename_directory = os.path.dirname(filename)
    output_template = f'{filename_directory}/working_kibot_template.yaml'
    #copy and overwrite the template file if it exists
    shutil.copyfile(template_file, output_template)

def push_to_git(**kwargs):
    repo_directory = kwargs.get('repo_directory', os.getcwd())
    count = kwargs.get('count', 1)
    #push to github
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("%%%%%%  pushing to github")
    #remove the lock file on thsi repo if it exists
    try:
        os.remove(".git/index.lock")
    except:
        pass
    print(f"pushing to {repo_directory}")
    import git 
    result = repo = git.Repo(repo_directory)
    print(result)
    result =  repo.git.add("*")
    print(result)
    result = repo.index.commit(f"comitting after {count} generations")
    print(result)

    result = origin = repo.remote(name='origin')
    result = origin.push()
    print(result)
    #subprocess.run(["git", "add", "*"])
    #subprocess.run(["git", "commit", "-m", f"comitting after {count} generations"])
    #subprocess.run(["git", "push"])


def get_footprint_pin_names(**kwargs):
    ##abandoned because names come from the symbol
    from kiutils.footprint import Footprint
    filename = kwargs.get('filename', None)
    
    footprint = Footprint().from_file(filename)


    pass

import oom_yaml
import oom_markdown

def load_bom_into_yaml(**kwargs):
    directory = kwargs.get('directory', None)
    yaml_file = f"{directory}/working.yaml"
    bom_file = f"{directory}/working_bom.csv"
    if os.path.exists(bom_file):
        files = []    
        #divider is a ;
        with open(bom_file, newline='' ) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                files.append(row)
        oom_yaml.add_detail(yaml_file=yaml_file, detail=["bom",files], add_markdown=True)

     #load working_bom_schematic.csv into an array
    bom_file = f"{directory}/working_bom_schematic.csv"
    if os.path.exists(bom_file):
        files = []    
        #divider is a ;
        with open(bom_file, newline='' ) as csvfile:
            #skip the first 6 lines
            for i in range(5):
                next(csvfile)

            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                files.append(row)
        oom_yaml.add_detail(yaml_file=yaml_file, detail=["bom_schematic",files], add_markdown=True)

    
    #load position_top
    bom_file = f"{directory}/working-top.pos"
    key = "position_top"
    load_positions(filename = bom_file, yaml_file=yaml_file, key=key)
    
    #load position_bottom
    bom_file = f"{directory}/working-bottom.pos"
    key = "position_bottom"
    load_positions(filename = bom_file, yaml_file=yaml_file, key=key)

    #add mounting hoes
    add_mounting_holes(yaml_file=yaml_file)
       

def load_positions(**kwargs):
    bom_file = kwargs.get('filename', None)
    yaml_file = kwargs.get('yaml_file', None)
    key = kwargs.get('key', None)
    if os.path.exists(bom_file):
        files = []    
        #divider is a ;
        with open(bom_file, newline='' ) as csvfile:
            #skip the first 5 lines
            for i in range(4):
                next(csvfile)

            #import fixed width column file i don't known the column widths and data starts on line 5
            import pandas
            df = pandas.read_fwf(csvfile)
            #get the column names
            columns = df.columns
            #get the data
            data = df.values
            #get the number of rows
            rows = len(data)
            #get the number of columns
            cols = len(columns)
            #loop through the rows
            for row in range(rows):
                #create a dict for the row
                row_dict = {}
                #loop through the columns
                for col in range(cols):
                    #add the column name and data to the dict
                    row_dict[columns[col]] = data[row][col]
                #add the dict to the files list
                files.append(row_dict)
            #remove the last element
            files.pop()
            oom_yaml.add_detail(yaml_file=yaml_file, detail=[key,files], add_markdown=True)


def add_mounting_holes(**kwargs):
    yaml_file = kwargs.get('yaml_file', None)
    yaml_directory = os.path.dirname(yaml_file)
    yaml_dict = oom_yaml.load_yaml_directory(directory=yaml_directory)
    mounting_holes = []
    if "position_top" in yaml_dict:
        try:
            for line in yaml_dict["position_top"]:
                package_l = str(line["Package"]).lower()
                tests = ["mountinghole", "mounting hole", "mounting-hole", "mounting_hole"]
                if any(x in package_l for x in tests):            
                    m_hole = {}
                    m_hole["x"] = float(line["PosX"])
                    m_hole["y"] = float(line["PosY"])
                    m_hole["package"] = line["Package"]
                    m_hole["value"] = line["Val"]
                    m_hole["ref"] = line["# Ref"]
                    #needs implementing
                    m_hole["size"] = "m3"
                    mounting_holes.append(m_hole)
            #process mounting holes
            #find min_x and min y and subtract
            min_x = 9999999
            min_y = 9999999
            max_x = -9999999
            max_y = -9999999
            for hole in mounting_holes:
                if hole["x"] < min_x:
                    min_x = hole["x"]
                if hole["y"] < min_y:
                    min_y = hole["y"]
                if hole["x"] > max_x:
                    max_x = hole["x"]
                if hole["y"] > max_y:
                    max_y = hole["y"]
            #subtract min_x and min_y from all the holes
            for hole in mounting_holes:
                hole["x"] -= min_x
                hole["y"] -= min_y


            #turn all holes "x" and "y" into strings
            for hole in mounting_holes:
                hole["x"] = str(hole["x"])
                hole["y"] = str(hole["y"])        
            


            if mounting_holes:
                oom_yaml.add_detail(yaml_file=yaml_file, detail=["mounting_holes",mounting_holes], add_markdown=True)
        except Exception as e:
            print(f"error adding mounting holes: {e}")
        