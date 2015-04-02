#!/usr/bin/python3

"""
Reads grouped strace output files and generates 
analysis of machine learning accuracy using sklearn.

@author: Noah Frazier-Logue (n.frazier.logue@nyu.edu)

"""

#print statements for debugging purposes

import numpy
from sklearn import *
import scipy
import re
from collections import Counter
import glob
import os.path
import time

from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import train_test_split

from sklearn.metrics import classification_report


data_array = []
target_array = []


def read_files():
    """
    Scans all subdirectories for text files and returns
    them in a list.

    @rtype: list
    @return file_paths: list of file paths for use with
                        file_process, etc.
    """
    
    file_paths = []
    file_paths = glob.glob(
        './chunked_files/*.txt')
#    print(file_paths)
    return file_paths

def file_process(path):
    """
    Opens the readout file of a command given 'cmd'
    and returns a dictionary with system calls and
    the number of times they're called

    @type cmd: string
    @param cmd: command to generate dictionary for.
    
    @rtype: dictionary
    @return counter_dict: dictionary containing
                          system calls and
                          corresponding counts.
    """
    
    
    #opens file and reads lines to text
    text = open(path, "r")
    lines = text.readlines()
    text.close()

    #command_pattern = re.compile("[\w]+[(]")

    array_size = 0
    command_array = []
##    for i in range(75):
##        #regex to identify function calls
##        result = re.search("[\w]+[(]", lines[i])
##        #only adds to list if result is valid
##        if result:
##            command = (result.group()).replace("(", "")
##            command_array.append(command)
##    

    for i in lines:
        #regex to identify function calls
        result = re.search("[\w]+[(]", i)
        #only adds to list if result is valid
        if result:
            command = (result.group()).replace("(", "")
            command_array.append(command)
    


    #counter module creates dictionary
    counter_dict = Counter(command_array)

    #debug print
#    for key, value in counter_dict.items():
#        print(key, "-", value)
        

    return counter_dict

def create_initial_array(file_paths):
    """
    Creates array that contains combined system calls
    of all commands passed in as arguments. This array
    is to be used in the creation of the sklearn vector
    later in the program.

    Note: duplicates are removed from this array.

    @rtype: list
    @return initial_array: array containing system calls.
    """
    
    initial_array = []

    #appends each system command from all passed in
    #commands given it's not already in the array
    for path in file_paths:
        temp_dict = file_process(path)
        for key, value in temp_dict.items():
            if key not in initial_array:
                initial_array.append(key)
    #sorts list alphabetically for clarity
    initial_array = sorted(initial_array, key=str.lower)
#    print(initial_array)
    return initial_array

def get_file_names(file_paths):
    """
    Parses file paths and returns file names for use
    with id_num, etc.

    @type file_paths: list
    @param file_paths: list of file paths

    @rtype: list
    @return file_names: file names to be used in
                        id_tag, etc.
    """

    file_names = []

    for path in file_paths:
        dir_name, file_ext = os.path.split(path)
        file, extension = os.path.splitext(file_ext)
        file_names.append(file)
    return file_names
        
    
def id_tag(cmd):
    """
    Generates unique id's for each file based on their
    file names. For use with sklearn's machine
    learning vector.

    @type cmd: string
    @param cmd: command to generate id for.

    @rtype: integer
    @return index: id number (index position) for
                   given command
    """

    id_tag = cmd.partition("_")[0]
    return id_tag

def create_vector(initial_array, file_paths):
    """
    Creates vector containing count of each system call
    for each command, followed by the id number for each
    command. For use with sklearn.

    @type initial_array: list
    @param initial_array: array that contains system calls
                          to be tallied.
    
    @rtype: list
    @return sklearn_array: array to be used with sklearn
                           module.
    """

    global data_array
    global target_array

    file_names = get_file_names(file_paths)

    #completes all operations for each command
    for i in range(len(file_names)):
        index = file_names.index(file_names[i])
        current_dict = file_process(file_paths[i])
        
        key_array = []
        value_array = []
        #puts keys in key_array and values in value_array
        for key, value in current_dict.items():
            key_array.append(key)
            value_array.append(value)
        #creates empty nummber array to put command
        #call counts in
        vector_nums = [0] * len(initial_array)
        #adds in same position as initial_array
        for h in range(len(initial_array)):
            for j in range(len(key_array)):
                if key_array[j] == initial_array[h]:
                    vector_nums[h] = value_array[j]
#        print(vector_nums)

        id_num = id_tag(file_names[i])
        #adds vector and id values to sklearn_array
        #to made 3d array (the final vector)

        data_array.append(vector_nums)
        target_array.append(id_num)
    
#    print(sklearn_array)

def sklearn_run(x, y):
    """
    Uses sklearn module to analyze data and
    print out results.

    @type x: np.array
    @param x: data vector in numpy array

    @type y: list
    @param y: id vector for use with np_data
    """
    clf = svm.SVC(kernel='linear', probability=True, C = 1)  

    scores = cross_validation.cross_val_score(
        clf, numpy.array(x),
        numpy.array(y), cv = 2, scoring = 'accuracy')

    print(scores)  
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    print()

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)
    y_pred = clf.fit(x_train, y_train).predict(x_test)

    cm = confusion_matrix(y_test, y_pred)

    print(cm)
    print()

    predictions = clf.predict(x)
    #print(predictions)
    expected = y

    print(classification_report(expected, predictions))
    

def main():
    """
    Program driver; calls all functions in the order they
    need to be called.
    """
    
    global data_array
    global target_array
    
    print("Creating vector...")
    start_time = time.time()
    file_paths = read_files()
    file_names = get_file_names(file_paths)
#    print(file_names)
    initial_array = create_initial_array(file_paths)
#    print(initial_array)
    sklearn_array = create_vector(initial_array, file_paths)
    #creates numpy array
    np_data = numpy.array(data_array)
    np_target = numpy.array(target_array)
    print("Done.")
#    print(np_data)
#    print(np_target)


    sklearn_run(np_data, np_target)
    total_time = time.time() - start_time
    print("Time taken: " + str(total_time) + "s")
    
   
main()
