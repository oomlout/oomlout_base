import PyPDF2
import os


def main(**kwargs):
    #print "loading parts" plus the module name get the module name from the filename using __name__
    
    print("merging pdfs")
    folder = kwargs.get("folder", os.getcwd())
    print(f"  folder: {folder}")
    pattern_match = kwargs.get("pattern_match", ["*.pdf"])
    file_output = kwargs.get("file_output", "merged.pdf")

    # get all the pdf files in the folder recursively
    pdf_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    # sort the pdf files by name
    pdf_files.sort()
    # create a pdf writer
    pdf_writer = PyPDF2.PdfWriter()
    # loop through the pdf files and add them to the writer
    for pdf_file in pdf_files:
        print(f"  adding {pdf_file}")
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # loop through the pages and add them to the writer
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

    # write the output file
    output_file = os.path.join(folder, file_output)
    # check if the output file already exists
    if os.path.exists(output_file):
        # if it does, delete it
        os.remove(output_file)
    # create the output folder if it doesn't exist
    output_folder = os.path.dirname(output_file)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with open(output_file, "wb") as f:
        output_file_abs = os.path.abspath(output_file)
        print(f"  writing {output_file_abs}")
        pdf_writer.write(f)







if __name__ == "__main__":
    # run the function
    kwargs = {}

    folder = os.getcwd()
    #folder = r"C:\od\OneDrive\docs\business_vintage_clothing_order_number_tag"
    


    kwargs["folder"] = folder



    main(**kwargs)

