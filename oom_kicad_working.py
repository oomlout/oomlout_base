import oom_kicad



def main():
    #set_components()
    board_file = rf"C:\GH\oomlout_electronics_oobb_led_matrix\kicad\working\working.kicad_pcb"
    oom_kicad.generate_outputs(board_file=board_file)

def set_components():
    ##### sample file in electronics matrix
    pass


if __name__ == '__main__':
    main()




