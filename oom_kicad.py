
from oomBase import *


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
    define_mouse_positions(**kwargs)
    generate_outputs_board(**kwargs)
    generate_outputs_schematic(**kwargs)

def generate_outputs_board(**kwargs):
    #get current working directory as a string
    import os
    current_working_directory = os.getcwd().replace("\\","/")

    filename = kwargs.get('filename', None)
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

    overwrite = True
    #get the directory of board_file and set dir to be it
    dir = os.path.dirname(board_file) + "/"
    #replace backslashes with slashes
    dir = dir.replace("\\","/")
    print("Harvesting Kicad Board File: " + kicadBoard)
    #test if the last 3d render exists if it does skip the rest
    if not os.path.isfile(dir + "working_3d.png"):
        oomLaunchPopen("pcbnew.exe " + kicadBoard,15)
        oomSendEnter(delay = 5)
        oomMouseMove(pos=kicadFootprintMiddle,delay=2)
        oomSend("b",10)
        oomMouseClick(pos=kicadActive,delay=5)  
        
        filename = dir
        filename = filename.replace("\\","/") 
        filename = filename.replace("//","/")
        oomMakeDir(filename)
        kicadExport(filename,"bom",overwrite=overwrite)
        kicadExport(filename,"pos",overwrite=overwrite)                
        kicadExport(filename,"svg",overwrite=overwrite)            
        #kicadExport(filename,"wrl",overwrite=overwrite)
        #kicadExport(filename,"step",overwrite=overwrite)
        kicadExport(filename,"3dRender",overwrite=overwrite)
        kicadClosePcb()    


def generate_outputs_schematic(**kwargs):   
    overwrite = kwargs.get('overwrite', False)
    #get current working directory as a string
    import os
    current_working_directory = os.getcwd()     
    board_file = kwargs.get('board_file', "none")
    if board_file == "none":
        board_file = kwargs.get('filename', rf"{current_working_directory}\oomp\current\working\working.kicad_pcb")
    #change to sch file
    board_file = board_file.replace(".kicad_pcb",".kicad_sch")
    #if board file doesn't start with a drive
    if not board_file[1] == ":":
        board_file = rf"{current_working_directory}\{board_file}"

    kicadBoard = board_file
    directory = os.path.dirname(board_file) + "/"
    imageFile = directory + "working_schematic.png"
    pdfFile = directory + "working_schematic.pdf"
    if os.path.isfile(kicadBoard):
        if overwrite or not os.path.isfile(imageFile):
            print("Harvesting Kicad Board File: " + kicadBoard)

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
            #maximize
            #oomSendMaximize()
            oomDelay(2)
            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomMouseMove(pos=kicadActive,delay=2)
            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomMouseMove(pos=kicadActive,delay=2)
            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomMouseMove(pos=kicadActive,delay=2)
            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomMouseClick(pos=kicadActive,delay=5)    
            
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
            src = f'{directory}tmp/working.pdf'
            dest = f'{directory}working_schematic.pdf'
            #delete if the dest exists
            if os.path.isfile(dest):
                os.remove(dest)
            if os.path.isfile(src):
                os.rename(src, dest)
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


def kicadExport(filename,type,overwrite=False):
    if type.lower() == "bom":        
        bomFile = filename + "working_bom.csv"
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
        bomFile = filename + "working.pos"
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
        if overwrite or not os.path.isfile(filename + "working-B_Cu.svg"):
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
    if type.lower() == "wrl":
        if overwrite or not os.path.isfile(filename + "working.wrl"):
            print("    Making wrl file")
            oomMouseClick(pos=kicadFile,delay=5)       
            oomSend("e",2)
            oomSend("v",5)
            oomSendShiftTab(2,delay=2)
            oomSendEnter(delay=2)
            oomSend("y",8)
            oomSendEsc(5)
    if type.lower() == "step":
        if overwrite or not os.path.isfile(filename + "working.step"):
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
        if overwrite or not os.path.isfile(filename + "working_3d.png"):
            filename = filename.replace("\\\\","\\")
            filename = filename.replace("//","/")
            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomSendAltKey("3",5)
            ###### zoom
            oomMouseClick(pos=kicad3dView,delay=1)
            oomSend("z")
            oomSendEnter(delay=1)
            ######  front
            currentFile = filename + "working_3d_front.png"
            oomMouseClick(pos=kicadFile,delay=5) 
            oomSend("e",2)
            oomSendEnter(delay=2)
            oomSend(currentFile.replace("/","\\"),2)
            oomSendEnter(delay=2)
            oomSend("y",2)
            ######  back
            currentFile = filename + "working_3d_back.png"
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

            currentFile = filename + "working_3d.png"
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
        #oomSendMaximize()
        oomMouseClick(pos=kicadFile,delay=5)
        oomSendDown(2,delay=2)
        oomSendEnter(delay=5)
        oomSend(kicad_schematic.replace("/","\\").replace("\\\\","\\"),2)
        oomSendEnter(delay=10)
        oomSend("y",2)
        oomSendEnter(delay=2)
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
        

def generate_readme(**kwargs):
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




    
    




    



