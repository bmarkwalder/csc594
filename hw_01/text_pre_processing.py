"""
Brandon Markwalder
CSC 594
Spring 2018
Homework 01 Text pre-processing

This program will tokenize a corpus such that words, leading and trailing
punctuation and expanded contractions are converted to tokens. Punctuation
found in the middle of a word is ignored. The program outputs the number of:
Sentences, paragraphs, tokens, types, and the token frequencies.

To run the program:
Save text_pre_processing.py and the input file to the same directory.
Open text_pre_processing.py in the Python interpreter and run the module.
By default, the program will look for sample.txt as the input file and write
output.txt as output file to the same directory in which text_pre_processing.py
is stored. The program will accept input and output file arguments from an IDE, however
if the arguments are malformed or the input file cannot be found, the program will exit.

Optionally the program can be run from the command line and supplied input
and output filearguments. Error checking has been kept to a minimum so again,
the program will exit if the argumentsare malformed or if the input file cannot be found.

To run the program from the command line on a windows machine:
Save the input file to the top level directory in which python.exe is located
and execute the following command: text_pre_processing.py -i <inputfile> -o <outputfile>
"""

import sys
import getopt
from nltk.tokenize import sent_tokenize
import string

#Open and read the input file
def read_file(path):

    words = []

    with open(path, 'r') as f:
        for line in f:
            for word in line.split():
                words.append(word)

    return words

#Recurrsively strip and tokenize punctuation from the end of each word
def process_end(words, pun):

    for word in words:
        if word[-1] in pun and len(word) > 1:
            words[(words.index(word))] = word[0:-1]
            words.append(word[-1])
            process_end(words, pun)

    return words

#Recurrsively strip and tokenize punctuation from the beginning of each word
def process_start(words, pun):

    for word in words:
        if word[0] in pun and len(word) > 1:
            words[(words.index(word))] = word[1:]
            words.append(word[0])
            process_end(words, pun)

    return words

#Process special case contractions
'''Check each word. If it exists in the dictionary, split the returned value
Replace the special case contraction with the leading split result and append
the trailing result to the list'''
def process_special(words):

    dict = {"Can't": "can not", "can't": "can not",
            "He's": "He is", "he's": "he is",
            "Here's": "Here is", "here's": "here is",
            "I'm": "I am","i'm": "i am",
            "It's": "It is", "it's": "it is",
            "She's": "She is", "she's": "she is",
            "That's": "That is", "that's": " that is",
            "There's": "There is", "there's": "there is",
            "Won't": "Will not", "won't": "will not"}

    for word in words:
        if word in dict:
            split = dict.get(word).split()
            words[(words.index(word))] = split[0]
            words.append(split[1])

    return words

#Process compound contractions by stripping the trailing contraction
'''Replace the compound contraction with the singular contraction in place
Do a dictionary lookup for the trialing contraction and append the value to the list'''
def process_compounds(words):

    dict = {'ll': 'will',
            "n't": 'not',
            've': 'have',
            'd': 'would',
            're': 'are'}

    for word in words:
        if word.find("'") != -1 and len(word) > 1:
            split = word.split("'")
            if len(split) > 2:
                words[(words.index(word))] = word[0:(len(word)-(len(split[2]))-1)]
                words.append(dict.get(split[2]))

    return words

#Process single contractions and possesives
'''Check each word and split if a possessive or contraction is found.
If the trailing split is equal to the string literal s, we replace the word in place with the leading split
and append the trailing split with a joined apostrophe because we lost it in the split operation.
If the trialing split is equal to the string literal t, slice the word such that we remove the sting literal n
and replace the word in place in the list. Then we append the resulting value of the dictionary lookup to the list.
All other split cases fall to the else block where the word is replaced with the leading split dictionary lookup and 
the trailing split dictionary lookup is appended to the list'''
def process_contractions(words):

    dict = {'ll': 'will',
            "t": 'not',
            've': 'have',
            'd': 'would',
            're': 'are'}

    for word in words:
        if word.find("'") != -1 and len(word) > 1:
            split = word.split("'")
            if split[1] == 's':
                words.append(split[0])
                words[(words.index(word))] = ('' .join(["'", split[1]]))
            elif split[1] == 't':
                words[(words.index(word))] = (split[0])[:-1]
                words.append(dict.get(split[1]))
            else:
                words[(words.index(word))] = split[0]
                words.append(dict.get(split[1]))

    return words

#Count the number of paragraphs
def find_paragraphs(lines):

    p_count = [line for line in lines if (line != '\n')]

    return p_count

#Count the number of sentences
def find_sentences(paragraphs):

    sentences = sent_tokenize(''.join(paragraphs))

    return sentences

#Compute word frequencies
'''Iterate through the tokenized list and add each item to the dictionary.
If the key exists, update the value by 1. If the key does not exists, it is added
to the dictionary with an initial value of 1.'''
def get_frequencies(words):

    freq = {}

    for item in words:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1

    return freq

#Read the file and tokenize the contents.
def tokenize(path):

    words = read_file(path)
    #Apply set() to String's puncuation list
    pun = set(string.punctuation)

    words = process_end(words, pun)
    words = process_start(words, pun)
    words = process_special(words)
    words = process_compounds(words)
    words = process_contractions(words)

    return words

#Gather outputs, sort the tokens, and write to disk
def write_to_file(words, INPUT_FILE_NAME, OUTPUT_FILE_NAME):

    lines = open(INPUT_FILE_NAME)
    paragraphs = find_paragraphs(lines)
    sentences = find_sentences(paragraphs)
    num_tokens = len(words)
    num_types = len(set(words))

    frequencies = get_frequencies(words)

    #Convert the frequency dictionary to a lexicographically sosrted list in ascending order
    frequencies = (sorted(frequencies.items(), key=lambda x: (x[0])))

    #Resort the list by frequency in decending order
    frequencies.sort(key=lambda x: (x[1]),  reverse=True)

    f = open(OUTPUT_FILE_NAME, 'w')
    f.write('# of paragraphs = ' + str(len(paragraphs)) + '\n')
    f.write('# of sentences = ' + str(len(sentences)) + '\n')
    f.write('# of tokens = ' + str(num_tokens) + '\n')
    f.write('# of types = ' + str(num_types) + '\n')
    f.write('================================' + '\n')

    for key, value in frequencies:
        f.write(str(key) + " " + str(value) + '\n')
    f.close()

#Main function
'''Takes .txt input and outputs .txt
If run in the Python interpreter and no arguments are passed, the program defaults
to the following arguments: input=sample.txt and output=output.txt
Main has limited error checking and will exit on malformed arguments or missing files
Main modifed from: https://www.tutorialspoint.com/python3/python_command_line_arguments.htm'''
def main(argv):

   inputfile = ''
   outputfile = ''

   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('text_pre_processing.py -i <inputfile> -o <outputfile>')
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print ('text_pre_processing.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   if len(inputfile) != 0:
       INPUT_FILE_NAME = inputfile
   else:
       INPUT_FILE_NAME = 'sample.txt'

   if len(outputfile) != 0:
       OUTPUT_FILE_NAME = outputfile
   else:
       OUTPUT_FILE_NAME = 'output.txt'

   print('Tokenizing ' + INPUT_FILE_NAME)
   print('Output written to ' + OUTPUT_FILE_NAME)

   tokens = tokenize(INPUT_FILE_NAME)
   write_to_file(tokens, INPUT_FILE_NAME, OUTPUT_FILE_NAME)


if __name__ == "__main__":
   main(sys.argv[1:])