import oom_markdown
import os
import argparse
import robo
import working_helper

#process
#  locations set in working_parts.ods 
#  export to working_parts.csv
#  put components on the right side of the board
#  run this script

def main(**kwargs):
    pass
    #make_readme(**kwargs)
    #working_helper.run_utility(**kwargs)
    kwargs["mode"] = "ai"
    working_helper.run_robo_ai(**kwargs)


        #get tempalte repo in
        
        

def make_readme(**kwargs):
    os.system("generate_resolution.bat")
    oom_markdown.generate_readme_project(**kwargs)
    #oom_markdown.generate_readme_teardown(**kwargs)


if __name__ == '__main__':
    # parse arguments
    argparser = argparse.ArgumentParser(description='project description')
    #--file_input -fi
    argparser.add_argument('--file_input', '-fi', type=str, default='', help='file_input')    
    args = argparser.parse_args()
    kwargs = {}
    # update kwargs with args
    kwargs.update(vars(args))

    
    
    
    
    main(**kwargs)