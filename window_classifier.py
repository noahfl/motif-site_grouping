#!/usr/bin/python3

"""
Reads strace outputs for all files in specified
folders and subfolders and chunks them into 75-line
output files.

Output files are stored in ./chunked_files/

@author: Noah Frazier-Logue (n.frazier.logue@nyu.edu)

"""

import glob
import os.path

def read_files():
    """
    Scans all subdirectories for text files and returns
    them in a list.

    @rtype: list
    @return file_paths: list of file paths for use with
                        file_process, etc.
    """
    
    file_paths = glob.glob(
        './output_files/*/*.txt')
    file_paths.sort()
#    print(file_paths)
    return file_paths

def get_folder_names(file_paths):
    """
    Parses file paths and returns folder names for use
    with split_files

    @type file_paths: list
    @param file_paths: list of file paths

    @rtype: list
    @return file_names: file names to be used in
                        id_tag, etc.
    """

    folder_names = []

    for path in file_paths:
        dir_name, file_ext = os.path.split(path)
        file, extension = os.path.splitext(file_ext)
        file_folder = file.partition("_")[0] + "_chunked"
#        print(file_folder)
        folder_names.append(file_folder)
    return folder_names

def split_files(file_paths, file_names, folder_names):
    """
    Reads each file in the designated subdirectories
    and separates them into 75-line chunks. It then
    writes those chunks to files in the destination
    directory.

    @type file_paths: list
    @param file_paths: array containing all file paths
                       in the designated subdirectories
    @type file_names: list
    @param file_names: array containing all file names
                       in the designated subdirectories
    """

    
    for r in range(len(file_paths)):
        folder = folder_names[r]
#        path = '/home/bearface/grive/Research/attribute_mining/chunked_files/' + folder +'/'
        path = './chunked_files/'
        if (os.path.isdir(path) != True):
            print(folder + " file not written.")
            continue
        #print(path)
        current = open(file_paths[r])
        current_file = current.readlines()
        current.close()
        #line counter for chunks
        chunk_num = 1
        line = 0
        fileout = open(
            (path + str(file_names[r]) + '_chunk_' + str(chunk_num) + '.txt'), 'w+')
        for i in range(len(current_file)):
            fileout.write(current_file[i])
            line += 1
            if (((line % 75) == 0) and (line > 0)):
                fileout.close()
#                print(path + str(file_names[r]) + '_chunk_' + str(chunk_num) + '.txt')
                chunk_num += 1
                fileout = open(
                    (path + str(file_names[r]) + '_chunk_' + str(chunk_num) + '.txt'), 'w+')
        cleanup(path)
    #print_counts(path)
    

def get_file_names(file_paths):
    """
    Parses file paths and returns file names for use
    with id_num, etc.

    @type file_paths: list
    @param file_paths: list of file paths

    @rtype: list
    @return file_names: file names to be used in
                        id_number, etc.
    """
    
    file_names = []

    for path in file_paths:
        dir_name, file_ext = os.path.split(path)
#        print(dir_name)
        file, extension = os.path.splitext(file_ext)
        file_names.append(file)
    return file_names

def cleanup(path):
    """
    Checks destination subdirectories to see if there
    are any files less than 75 lines long and deletes
    them.

    @type path: string
    @param path: directory that holds output files
    """
    
    output_files = glob.glob(path + '*.txt')
    for i in range(len(output_files)):
        with open(output_files[i], 'r') as file:
            count = sum(1 for line in file)
#            print(count)
        if (count < 75):
            os.remove(output_files[i])

def print_counts(path):
    """
    Debugging function that prints line counts for files
    in destination directory

    @type path: string
    @param path: directory that holds output files
    """
    
    output_files = glob.glob(path + '*.txt')
    output_files.sort()
    for i in range(len(output_files)):
        count = 0
        file = open(output_files[i], 'r')
        for line in file:
            count += 1
#        print(output_files[i][-18:-1], count)

def main():
    """
    Program driver; calls all functions in the order they
    need to be called.
    """

    print("Chunking files...")
    file_paths = read_files()
    file_names = get_file_names(file_paths)
    folder_names = get_folder_names(file_paths)
    split_files(file_paths, file_names, folder_names)
    print("Done.")

main()
