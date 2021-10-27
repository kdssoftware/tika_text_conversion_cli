#!/usr/bin/env python3
import argparse
from tika import parser
import os

allowed_exstensies = ["odt", "pptx", "pdf", "ppt", "tex", "doc", "docx", "rtf"]


def main():
    # start tool
    try:
        ## ARGUMENTS ##
        arg_parser = argparse.ArgumentParser(description='File to text conversion.')
        arg_parser.add_argument("-f", "--file", help="[Required] Give path of source file")
        # optional
        arg_parser.add_argument("-s", "--save", help="[Optional] Save ouput in file")
        arg_parser.add_argument("-d", "--debug", help="[Optional] Debug mode, shows more info and error messages", action="store_true")
        arg_parser.add_argument("-m", "--meta-data", help="[Optional] Instead of text ouput, shows metadata as ouput", action="store_true")
        args = arg_parser.parse_args()

        debug = args.debug 
        file = args.file
        savePath = args.save 
        metadata = args.meta_data

        if debug:
            print("Arguments:")
            print(args)

        ## CHECKS ##
        # check if file is given
        if file == None:
            if debug:
                print("No source file argument give, show help message")
            # toon help
            arg_parser.print_help()
            return 2
        # check if file exist
        if not os.path.isfile(file):
            print("Given source file does not exist")
            return 3

        # check if file exstenstion is allowed
        if (check_extensie(file)) == False:
            print("This tool only allows the following file extensions: " + str(allowed_exstensies))
            exit()

        ## CONVERSION ##
        # Parse data from file
        file_data = parser.from_file(file)
        output = ""
        if metadata:
            output = file_data["metadata"]
        else:
            output = file_data["content"]
        
        if debug:
            print("Length of output: " + str(len(output)))

        if savePath != None:
            # if save is given, save as file
            with open(savePath, "a", encoding="UTF-8") as f:
                f.write(str(output))
        else:
            if debug:
                print("--OUTPUT------------------------")
                print(output)
                print("--------------------------------")
            else:
                print(output)

        # stop tool
        return 0
    except Exception as e:
        # On error, stop program
        print("Something went wrong, try using debug mode -d")
        if debug:
            print(e)
        return 1


# functies

def check_extensie(path):
    extensie = path.split(".")[-1]
    if extensie in allowed_exstensies:
        return True
    else:
        return False


if __name__ == '__main__':
    main()
