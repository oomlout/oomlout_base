
from oomBase import *


from kiutils.board import Board
from kiutils.items.common import Position

def kicad_set_components(**kwargs):
    board_file = kwargs.get('board_file', None)
    board_file = board_file.replace('\\', '/')
    components = kwargs.get('components', None)    

    board = Board.from_file(board_file)
    footprints = board.footprints
    for component in components:
        for footprint in footprints:        
            #get reference by going through components.graphicItems until typw is 'reference' then make ref equal to text
            reference = None
            for graphicItem in footprint.graphicItems:
                try:
                    if graphicItem.type == 'reference':
                        reference = graphicItem.text
                except:
                    pass
                    #skip lines and rectangles

            if reference == component['reference']:
                current_pos = footprint.position                
                
                new_pos = component.get('position', current_pos)
                if len(new_pos) == 2:
                    new_pos = (new_pos[0], new_pos[1], 0)
                corel_pos = component.get('corel_pos', False)
                if corel_pos:                       
                    corel_p = get_from_corel_coord(new_pos[0], new_pos[1]  )
                    new_pos = (corel_p[0], corel_p[1], new_pos[2])
                new_pos = Position(new_pos[0], new_pos[1], new_pos[2])
                footprint.position = new_pos
                
    
    board.filePath = board.filePath.replace('.kicad_pcb', '_new.kicad_pcb')
    board.to_file()

def get_from_corel_coord(x,y):
    x = x
    y = -y
    return (x,y)


def generate_outputs(**kwargs):
    #get current working directory as a string
    import os
    current_working_directory = os.getcwd()


    board_file = kwargs.get('board_file', f"{current_working_directory}\kicad\working\working.kicad_pcb")
    kicadBoard = board_file
    overwrite = True
    #get the directory of board_file and set dir to be it
    dir = os.path.dirname(board_file) + "/"
    print("Harvesting Kicad Board File: " + kicadBoard)
    #test if the last 3d render exists if it does skip the rest
    if not os.path.isfile(dir + "kicad_pcb_3d.png"):
        oomLaunchPopen("pcbnew.exe " + kicadBoard,10)
        oomSendEnter(delay = 5)
        oomMouseMove(pos=kicadFootprintMiddle,delay=2)
        oomSend("b",10)
        oomMouseClick(pos=kicadActive,delay=5)    
        filename = dir
        oomMakeDir(filename)
        kicadExport(filename,"bom",overwrite=overwrite)
        kicadExport(filename,"pos",overwrite=overwrite)                
        kicadExport(filename,"svg",overwrite=overwrite)            
        kicadExport(filename,"wrl",overwrite=overwrite)
        kicadExport(filename,"step",overwrite=overwrite)
        kicadExport(filename,"3dRender",overwrite=overwrite)
        kicadClosePcb()    


kicadActive =[515,14]
kicadFile = [80,35]
kicadFootprintMiddle = [945,545] 
kicad3dView = [145,35]

def kicadExport(filename,type,overwrite=False):
    if type.lower() == "bom":        
        bomFile = filename + "kicad_board_bom.csv"
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
        bomFile = filename + "kicad_board.pos"
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
        if overwrite or not os.path.isfile(filename + "kicad_board-B_Cu.svg"):
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
        if overwrite or not os.path.isfile(filename + "kicad_board.wrl"):
            print("    Making wrl file")
            oomMouseClick(pos=kicadFile,delay=5)       
            oomSend("e",2)
            oomSend("v",5)
            oomSendShiftTab(2,delay=2)
            oomSendEnter(delay=2)
            oomSend("y",8)
            oomSendEsc(5)
    if type.lower() == "step":
        if overwrite or not os.path.isfile(filename + "kicad_board.step"):
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
        if overwrite or not os.path.isfile(filename + "kicad_pcb_3d.png"):

            oomMouseMove(pos=kicadFootprintMiddle,delay=2)
            oomSendAltKey("3",5)
            ###### zoom
            oomMouseClick(pos=kicad3dView,delay=1)
            oomSend("z")
            oomSendEnter(delay=1)
            ######  front
            currentFile = filename + "kicad_pcb_3d_front.png"
            oomMouseClick(pos=kicadFile,delay=5) 
            oomSend("e",2)
            oomSendEnter(delay=2)
            oomSend(currentFile.replace("/","\\"),2)
            oomSendEnter(delay=2)
            oomSend("y",2)
            ######  back
            currentFile = filename + "kicad_pcb_3d_back.png"
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

            currentFile = filename + "kicad_pcb_3d.png"
            oomMouseClick(pos=kicadFile,delay=5) 
            oomSend("e",2)
            oomSendEnter(delay=2)
            oomSend(currentFile.replace("/","\\"),2)
            oomSendEnter(delay=2)
            oomSend("y",2)
            ###### close
            oomMouseClick(pos=kicadFile,delay=5) 
            oomSend("c",2)

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



def generate_readme(**kwargs):
    import oomp
    oomp.load_parts(make_files=False)
    name = kwargs.get('name', None)
    description = kwargs.get('description', None)

    # time to make a readme for the provided project
    readme = f"# {name}\n"
    # if the file kicad/working/kicad_pcb_3d.png exists add it
    if os.path.isfile("kicad/working/kicad_pcb_3d.png"):
        readme += f"![{name}](kicad/working/kicad_pcb_3d.png)\n"
    # add description with header 
    readme += f"## Description\n"
    readme += f"{description}/\n"
    # add the bom if it exists
    if os.path.isfile("kicad/working/kicad_board_bom.csv"):
        readme += f"## Bill of Materials\n"
        #take the bom csv and import it as a dict using csv library don't add it to bom do it in one line rather than using a csvfile object it is seperated with ;
        bom = csv.DictReader(open("kicad/working/kicad_board_bom.csv"), delimiter=';')
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
            
            


            

        

        
            
            
        
        
        # add extra images in the base directory and in the kicad/working directory check go through the directory to find them
    readme += f"\n## Images\n"
    #find all the pngs in the base directory and kicad/working
    pngs = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".png"):
                pngs.append(os.path.join(root, file))   
    #add them to the readme
    for png in pngs:
        #add each png as a lnked image
        png = png.replace(".\\", "")
        png = png.replace("\\", "/")
                          
        readme += f"![{png}]({png})\n"
        
    #write the readme
    with open("readme.md", "w") as f:
        f.write(readme)
    




    
    




    




