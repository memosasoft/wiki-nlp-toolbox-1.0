# Python program to AI learning from reading text data
from datetime import datetime

import os
## Importing Necessary Modules
import requests     # to get image from the web
import shutil       # to save it locally
import datetime     # user for unique file name
import time         # used for sleep relax function
import urllib.parse

#import text_tools as txt_tool

MIN_KEYWORD_LEN = 1 
MAX_KEYWORD_LEN = 25 

KEYWORD_MATRIX_LIMIT = 20
MIN_LENGTH_OF_KEYWORD = 2

RELAX_TIME = 0

# Learning settings 
# Should be dynamique depending on the size of document
# Quality score determine how many hit needed to incorporate keyword
QUALITY_SCORE  = 7

concept = " "
keywords = {}   
related_keywords = {} 
unrelated_keywords = {} 
unclassified_keywords = {} 
sub_concepts = []
sub_unclassified_concepts = []
related_keywords_long_sentences = []
sub_unclassified_concepts_long_sentence = []

document = [concept, 
            keywords, 
            related_keywords,
            unrelated_keywords,
            sub_concepts,
            sub_unclassified_concepts,
            related_keywords_long_sentences,
            sub_unclassified_concepts_long_sentence]  

def start_program():
    
    # Program intro
    print("WELCOME TO MY WIKI-AI-NERD\n") 
    print("------------------------------")         
    print("Python AI - self-learning program")
    #print("This is a prototype with NLP")  
    print("Using Wikipedia data to train program")
    #print("--------------------------------------")   
    print("Developped Doctor g.- drg ") 
    print("help: gfm.mail.72@gmail.com")
    
    relax(RELAX_TIME)
    
    # Start reading folder with wiki text
    # the text where downloaded with another 
    # python program: 
    # wiki_smart_url_spider.py
    
    # preformate downloaded WIKI Documents 
    # before starting reading and learning 
    # txt_tool.read_files() - text_tools.py
    
    read_files()
    
def read_files():
    
    # user interaction to help understand program flow
    # print("STARTING READING WIKI LOCAL FILES")
    # print("Document path :")
    
    # Set the path where the wiki documents are found
    PATH = "/home/dr-g/Projet/Programmation/Python/smart-wiki-url-spider/spider"
    
    # Set the path
    files = os.listdir(PATH)
    # print(str(PATH))

    #print("MAIN LOOP - STARTED")

    # iterate thru all files in the folder
    for file_name in files:

        # print("Getting document in the folder...")
        relax(RELAX_TIME)
        
        # Getting document in the folder
        with open(PATH + "/" + file_name, "r") as file: 
            # reading each line     
            text_content = file.read()
            file.close() 

        # print("Transfer text information into local buffer...")
        # relax(RELAX_TIME)

        with open("buffer.txt", "w") as file: 
            # reading each line     
            file.write(text_content)
            file.close() 

        # transfer text information into buffer
        subject = clean_title(file_name)   
        # print("MAIN SUBJECT: " + subject)
        # relax(RELAX_TIME)
                
        # start first loop reading process 
        # looking for keyword matrix
        print("STARTING reading process and learning process")
        # print("Building keyword matrix for subject " + subject)
        
        document = read_and_learn(subject)
        # relax(RELAX_TIME)

        print("STARTING MEMORY SIGNATURES CREATION PROCESS")    
        #document = generate_keyword_signatures(subject) 
        #relax(RELAX_TIME)
                
        print("STARTING MEMORY LARGE SIGNATURES CREATION PROCESS")
        #document = save_in_memory(subject)
        #relax(RELAX_TIME)
        
        print("STARTING FINAL CLEANING PROCESS")
        # clean memory before next loop
        document = clean_memory(document)
        relax(RELAX_TIME)
        
#This function cleans the document title
def clean_title(file_name):
    
    # subject string variable  
    subject = format_filename(file_name)
    
    if (subject==None) or (subject==""):
        return ""
        
    # clean the filename to convert into text subject
    for word in file_name.split():
        # clean problematic char from title string
        word = clean_word_noise(word)

        # concatenate subject
        subject = subject + " " + word
        subject = trim(subject)
        
    return subject

def format_filename(file_name):
    # add url decoder to convert all char to readeable text
    file_name = urllib.parse.unquote(file_name)
    file_name = file_name.replace("_", " ")
    file_name = file_name.replace(".txt", " ")
    file_name = trim(file_name)
    
#This function read the texte
def read_and_learn(concept):
    
    global document
    global keywords
        
    #print("DOCUMENT TITLE IS : " + concept)  
    #print("STARTING KEYWORD EXTRACTION FOR TEXT BUFFER")  
    
    #relax(RELAX_TIME)
    
    PATH = "/home/dr-g/Projet/Programmation/Python/wiki-nerd/"
    files = os.listdir(PATH)   
            
    with open("buffer.txt","r") as file: 
        # reading each line
        for line in file: 
            
            line = clean_wiki_noise_from_line(line)
            line = check_line_stop_sentences(line)
            line = check_line_for_stop_code(line)
           
            if line == "":
                continue
            
            if len(line) < 1:
                continue    
            
            # THE UGLY FUNCTION
            line = catch_menu(line)
            
            # returns the line with minimal text processing
            # returns the clean_line with full text processing
            line, clean_line = line_cleansing(line) 
            
            if clean_line == "" or line == "":
                continue
            
            # reading each word       
            for word in clean_line.split():
                
                if len(word) < 1 or word == None or word == "":
                    continue
                
                # Final word clean up 
                word = clean_again_alien(word)
                word = clean_word_seperation(word)               
                word = clean_word_final(word)
                keywords = verify_keyword_frequency(word)
    
        file.close()
    
    print_keyword_matrix(concept)
        
    return document

def print_keyword_matrix(concept):
    keywords = sort_keyword_matrix()
    
    matrix_limit = KEYWORD_MATRIX_LIMIT
    
    list_keyword = []
    list_weight = []
    
    # output keyword matrix
    for keyword in keywords:
        list_keyword.append(keyword) 
        list_weight.append(keywords[keyword])

    list_keyword.reverse()
    list_weight.reverse()
    
    index = 0
    print("CONCEPT LEARNED IS: " + concept)
    for keyword in list_keyword:
        
        if (len(keyword)>MIN_LENGTH_OF_KEYWORD):
        
            weight = list_weight[index]
            
            print("[" + keyword + "," + str(weight)+"]")
            
            if keyword.isnumeric():
                matrix_limit = matrix_limit + 1
                
            if matrix_limit > 0:
                matrix_limit = matrix_limit - 1
                index = index + 1
            else:
                break
        
def clean_again_alien(word):
    if (len(word)-1>0):
        if word[len(word)-1] == ".":
            word = word[0:len(word)-1]
        if word[len(word)-1] == ",":
            word = word[0:len(word)-1]
        if word[len(word)-1] == ":":
            word = word[0:len(word)-1]
        if word[len(word)-1] == ";":
            word = word[0:len(word)-1]
    return word
    
def sort_keyword_matrix():
    global keywords
    
    sorted_values = sorted(keywords.values()) # Sort the values
    sorted_dict = {}

    for i in sorted_values:
        for k in keywords.keys():
            if keywords[k] == i:
                sorted_dict[k] = keywords[k]
                continue
            
    return sorted_dict

def generate_keyword_signatures(concept): 
    
    global document
     
    print("Starting reading buffer")    
    
    with open("buffer.txt","r") as file: 
        # reading each line
        for line in file: 
            
            # eliminate noise preformate
            # text clean up 
            # eliminates scripts code, wiki sections, end of section)
            line = clean_wiki_noise_from_line(line)
            
            if line == "" or len(line) < 1:
                continue          
            
            line, clean_line = line_cleansing(line)
            
            if clean_line == "" or line == "":
                continue
            
            # try to classify information being read by the signature(concept, line, document) 
            
            # save line signature to teach the systems memory
            save_signature(concept, line, document)
            
        file.close()
        
        print("Finished reading buffer")    
    
    return document

# MY UGLY FUNCTION
# ITS UGLY BUT IT WORKS
def catch_menu(line):
    
    try:
        # convert into recursive function
        if (line[0].isnumeric()):
            if len(line)>1:
                if (line[1]==" "):
                    line = line[2:len(line)]   
                if (line[1]=="."): 
                    if len(line)>2:    
                        if (line[2].isnumeric()): 
                            if len(line)>3:
                                if (line[3]==" "):
                                    line = line[4:len(line)]  
                                if (line[3]=="."): 
                                    if len(line)>5:  
                                        line = line[6:len(line)]
        return line
    except:
        print("ERROR - In UGLY function")                                
        return line
                
def verify_line_signature(concept, line, document):

    global keywords 
    global related_keywords
    global unrelated_keywords 
    global sub_concepts 
    global sub_unclassified_concepts 
    global related_keywords_long_sentences 
    global sub_unclassified_concepts_long_sentence 

    # TODO DEBUG - Add high keywords to concept
    concept = extended_concept(concept, keywords)
  
    # Deep clean free concepts    
    line, clean_line = line_cleansing(line)
            
    if (clean_line == "") or (line == ""):
        return document

    concept, clean_concept = line_cleansing(concept)
    
    if (concept==line):
        related_keywords = insert_in_memory(line_with_concept, related_keywords)       
  
    # DEBUG - EXPERIMENTAL QUERY EXPANSION
    no_match = True
    
    word_counter = len(line.split())
    
    for word in line.split(): 
        for concept_keyword in concept.split(): 
            for word_in_line in line.split(): 
                if word_in_line == concept_keyword:
                    no_match = False
                    if (word_counter>3):
                        if (word_counter<30):
                            related_keywords = insert_in_memory(line, related_keywords)
                        else:    
                            related_keywords_long_sentences.append(line)
                        break
                    else:
                        if not line in sub_concepts:
                            sub_concepts.append(line)
                
                if no_match == False:            
                    break
            if no_match == False:
                break 
        
        word_counter = len(line.split())
            
        if no_match == True:
            if (word_counter>3):
                if (word_counter<10):
                    unrelated_keywords = insert_in_memory(line, unrelated_keywords)
                else:
                    sub_unclassified_concepts_long_sentence.append(line)
            else:
                if not line in sub_unclassified_concepts:
                    sub_unclassified_concepts.append(line)
    
    return document

def extended_concept(concept, keywords): 

    extended_concept_keywords = 10
    
    sorted_values = sorted(keywords.values(), reverse=True) # Sort the values
    sorted_dict = {}

    lim = 0
    for i in sorted_values:
        for concept in keywords.keys():    
            if keywords[concept] == i:  
                sorted_dict[concept] = keywords[concept]
                if lim > extended_concept_keywords:
                    break
                lim = lim + 1
        if lim > 10:                
            break            
    x = 0

    for keyword in sorted_dict:
        if x < 10:
            concept = concept + " " + keyword
            x = x + 1
    return concept 

def extract_text_stats(document_stats): 
    
    number_of_lines = 0
    number_of_words = 0
    PATH = "/home/dr-g/Projet/Programmation/Python/wiki-AI/"
    files = os.listdir(PATH)   
   
    with open("buffer.txt","r") as file: 
        # reading each line
        for line in file: 
            # reading each word  
            number_of_lines = number_of_lines + 1

            for word in line.split():
                number_of_words = number_of_words + 1               
                
        file.close()

    document_stats = [number_of_lines, number_of_words]

    return document_stats

def debug_log(debug_info): 
    f = open("debug.log", "a+")
    f.write("\n" + str(debug_info))
    f.write("\n")
    f.close

def verify_keyword_frequency(word):
    # verify keyword 
    memory = insert_in_memory(word)
    return memory

def save_in_memory(concept): 
    
    global document
    
    if (concept == ""):
        return ""
    
    global keywords 
    global related_keywords
    global unrelated_keywords 
    global sub_concepts 
    global sub_unclassified_concepts 
    global related_keywords_long_sentences 
    global sub_unclassified_concepts_long_sentence 
  
    list_of_keywords = keywords
    
    counter = 0
    short_signature = ""
    
    for concepts in list_of_keywords:
        short_signature = short_signature + "-" + concepts
        if (counter > 3):
            break
        counter = counter + 1
    
    #Save all document information in memory
    concept, clean_concept = line_cleansing(concept) 
    concept, clean_short_signature = line_cleansing(short_signature) 
    
    clean_concept = concept.replace(" ","-")
    clean_concept = concept.replace("_","-")
    clean_concept = concept.replace("\\","-")
    clean_concept = concept.replace("/","-")
    clean_concept = clean_concept.lower()
   
    short_signature = short_signature.replace(" ","-")
    short_signature = short_signature.replace("_","-")
    short_signature = short_signature.replace("\\","-")
    short_signature = short_signature.replace("/","-")
    short_signature = short_signature.lower() 
    
    if (clean_concept=="") or (short_signature==""):
        return ""
        
    dateTimeObj = datetime.datetime.now()
    
    if len(list_of_keywords) > 10 and len(list_of_keywords) < 100:
        f = open("./memory/sig-"  + str(len(list_of_keywords)) + "-" + clean_concept + "-" + short_signature + "-" + dateTimeObj.strftime("%Y%m%d.txt"), "w")
    elif len(list_of_keywords) > 3 and len(list_of_keywords) < 10:
        f = open("./memory_small/sig-"  + str(len(list_of_keywords)) + "-" + clean_concept + "-" + short_signature + "-" + dateTimeObj.strftime("%Y%m%d.txt"), "w")
    else:
        return None  
    
    list_of_keywords_for_summary = []
    
    f.write("concept:\n")
    f.write(concept)
    f.write("\n")
    f.write("\n")
    f.write("KEYWORDS:\n")
    f.write("\n")

    # TODO - Insert sort algorithm into function
 #   summarize = sorted(list_of_keywords.values(), reverse=True) # Sort the values
 #   sorted_dict = {}

 #   for i in summarize:
 #       if i <= QUALITY_SCORE:
 #           break
#
 #       for key in list_of_keywords.keys():
 #           if list_of_keywords[key] == i:
 #               sorted_dict[i] = list_of_keywords[key]
            
 #               f.write("["+key+","+str(list_of_keywords[key])+"] ") 
 #               list_of_keywords.pop(key)
 #               list_of_keywords_for_summary.append(key)
 #               break
    
 #   list_of_keywords = sorted_dict

    f.write("\n")
    f.write("\n")
    f.write("GLOBAL KEYWORDS ARRAY:\n")
    f.write("\n")

    noise_list_of_keywords = keywords 
    for noise in noise_list_of_keywords.keys():
        f.write("["+noise+","+str(noise_list_of_keywords[noise])+"], ") 


    f.write("\n")
    f.write("\nOTHER RELATED SHORT CONCEPTS - with top frequency keywords match\n\n")
    
    for sub_concept in sub_concepts:
        f.write("["+sub_concept+"]\n")

    f.write("\n")
    f.write("\nOTHER UNCLASSIFIED CONCEPTS\n\n")
    
    for sub_unclassified_concept in sub_unclassified_concepts:
        f.write("["+sub_unclassified_concept+"]\n")
 

    f.write("\n")
    f.write("\nRELATED CONCEPTS LONG SENTENCE - with top frequency keywords\n\n")
    
    for long_sentence in related_keywords_long_sentences:
        f.write("["+long_sentence+"]\n")

    f.write("\n")
    f.write("UNCLASSIFIED CONCEPTS LONG SENTENCE\n\n")
    
    for long_sentence in sub_unclassified_concepts_long_sentence:
        f.write("["+long_sentence+"]\n")

    f.write("\n")
    f.write("DOCUMENT STATS\n\n")
   
    number_of_lines = 0
    number_of_words = 0

    document_stats = [number_of_lines, number_of_words]
    document_stats = extract_text_stats(document_stats)
    
    f.write("[number of lines in document: "+str(document_stats[0])+"]\n")
    f.write("[number of words in document: "+str(document_stats[1])+"]\n")

    f.close()
    
    return document
    
def summarize(list_of_keywords):  
    summary = " "
    phrase_limit = 0

    min_words_for_summary_line = 15
    summary_keyword_matches = 3
    number_of_phrases_in_summary = 3
    keywords_line_hits = 0
    # opening the text file  
    with open("text_data.txt","r") as file: 
        # reading each line
        for line in file: 
            words_in_line = 0
    
            # String pre formating
            line = line.strip()

            if (verify_quality_of_line(line) == False):
                continue

            # Count the line words
            words_in_line=len(line.split()) 
            
            # add new line 
            if (words_in_line>min_words_for_summary_line): 
                for word in line.split():
                    
                    word, clean_word = line_cleansing(word) 
                    if len(word)>1:
                        if word in list_of_keywords:
                            # number of summary lines
                            if phrase_limit <= number_of_phrases_in_summary :
                                if keywords_line_hits >= summary_keyword_matches :
                                    summary = summary + "\n\n" + line
                                    phrase_limit= phrase_limit + 1
                                    break
                                else:
                                    keywords_line_hits= keywords_line_hits + 1
                else:
                    continue 

                                 
        return summary
     
def save_signature(concept, signature, document):
   
    global keywords 
    global related_keywords
    global unrelated_keywords 
    global sub_concepts 
    global sub_unclassified_concepts 
    global related_keywords_long_sentences 
    global sub_unclassified_concepts_long_sentence 
    
    if len(signature) < 1:
        return False 
    
    print("CONCEPT: " + concept)
    
    # dictionnary list object
    list_keywords_signature = {} 
    
    # add concept keywords to signature
    for word in concept.split():
        if word in list_keywords_signature:
            list_keywords_signature[word] = list_keywords_signature[word] + 1
        else: 
            list_keywords_signature[word] = 1
        
    print("signature: " + signature)
    
    if (concept=="") or (signature==""):
        return ""
    
    counter = 0
    short_signature = ""
    
    for concepts in signature.split():
        # keyword too long elimination
        # NEED TO TEST - MAYBE A LIMITATION 
        # IS IT GOOD OR NOT? 
        if (len(concepts)>MAX_KEYWORD_LEN):
            return ""
        
        short_signature = short_signature + "-" + concepts
        if (counter > 3):
            break
        counter = counter + 1
    
    concept, clean_concept = line_cleansing(concept) 
    short_signature, clean_short_signature = line_cleansing(short_signature) 
    
    if (clean_concept=="") or (short_signature==""):
        return "" 
    
    short_signature = short_signature.replace(" ", "-")
    short_signature = short_signature.replace("_", "-")
    short_signature = short_signature.replace("\\", "-")
    short_signature = short_signature.replace("/", "-")
    short_signature = short_signature.replace(".txt", "")
    short_signature = short_signature.lower()
    
    clean_concept = clean_concept.replace(" ", "-")
    clean_concept = clean_concept.replace("_", "-")
    clean_concept = clean_concept.replace("\\", "-")
    clean_concept = clean_concept.replace("/", "-")
    clean_concept = clean_concept.replace(".txt", "")
    clean_concept = clean_concept.lower()
    
    if (clean_concept=="") or (short_signature==""):
        return ""
    
    dateTimeObj = datetime.datetime.now()
    
    PATH = "/home/dr-g/Projet/Programmation/Python/wiki-AI/"
    files = os.listdir(PATH)   
    
    if len(signature.split()) > 10  and len(signature.split()) < 100 :
        PATH = "/home/dr-g/Projet/Programmation/Python/wiki-AI/memory/sig-"
    elif len(signature.split()) > 3  and len(signature.split()) < 10 :
        PATH = "/home/dr-g/Projet/Programmation/Python/wiki-AI/memory_small/sig-" 
    else:
        return None  
    
    f = open(PATH + str(len(signature.split())) + "-" + str(clean_concept) + "-" + str(short_signature) + "-" + dateTimeObj.strftime("%Y%m%d.txt"), "w")
    f.write("concept:\n")
    f.write(concept)

    signature, clean_signature = line_cleansing(signature) 
    clean_signature = trim(clean_signature)
    
    if len(clean_signature) < 1:
        return False 
 
    f.write("\n\nSIGNATURE TITLE:\n\n ")
    f.write(concept)
    
    for word in clean_signature.split():
        if word in list_keywords_signature:
            list_keywords_signature[word] = list_keywords_signature[word] + 1
        else: 
            list_keywords_signature[word] = 1

    f.write("\n\nSIGNATURE:\n\n ")
    f.write(signature)
    
    relax(RELAX_TIME)

    f.write("\n\nFULL KEYWORD SIGNATURE LISTE:\n ")

    sorted_values = sorted(list_keywords_signature.values(), reverse=True) # Sort the values
    sorted_dict = {}
    for i in sorted_values:
        for concept in list_keywords_signature.keys():
            if list_keywords_signature[concept] == i:
                sorted_dict[concept] = list_keywords_signature[concept]
                
    list_keywords_signature = sorted_dict    
    
    for LISTE in list_keywords_signature:
        f.write("["+LISTE+","+str(list_keywords_signature[LISTE])+"] ")
        print("["+LISTE+","+str(list_keywords_signature[LISTE])+"] ")
        
    relax(RELAX_TIME)

    f.write("\n")
    f.write("DOCUMENT STATS\n\n")
    f.write("\n")
    
    number_of_lines = 0
    number_of_words = 0

    document_stats = [number_of_lines, number_of_words]
    document_stats = extract_text_stats(document_stats)
    
    f.write("[number of lines in document: "+str(document_stats[0])+"]\n")
    f.write("[number of words in document: "+str(document_stats[1])+"]\n")

    f.close()

    return document

def insert_in_memory(word):
    
    global keywords 
    
    if word in keywords:
        keywords[word] = keywords[word] + 1
    else: 
        keywords[word] = 1
    return keywords

def verify_quality_of_line(line):
    
    # Reset de word counter with new line
    words_in_line = 0
    quality_line_check = False

    # Count the line words
    for word in line.split(): 
        if len(word)>20:
            return quality_line_check

        # Add a word to the line  
        words_in_line=words_in_line+1 
   
    if words_in_line<1:
        return quality_line_check

    if words_in_line>100:
        return quality_line_check

    if len(line)<1:
        return quality_line_check

    if len(line)>2000:
        return quality_line_check

    s = line[0:1]
    if s.isupper() == False:
        return quality_line_check

    if line.find(".") < 1:
       return quality_line_check

    return True

#This function cleans the document title
def clean_memory(document):
    
    global concept
    global keywords  
    global related_keywords 
    global unrelated_keywords 
    global unclassified_keywords 
    global sub_concepts
    global sub_unclassified_concepts 
    global related_keywords_long_sentences 
    global sub_unclassified_concepts_long_sentence 

    concept = " "
    keywords = {}   
    related_keywords = {} 
    unrelated_keywords = {} 
    unclassified_keywords = {} 
    sub_concepts = []
    sub_unclassified_concepts = []
    related_keywords_long_sentences = []
    sub_unclassified_concepts_long_sentence = []
    
    document = [concept, 
                keywords, 
                related_keywords,
                unrelated_keywords,
                sub_concepts,
                sub_unclassified_concepts,
                related_keywords_long_sentences,
                sub_unclassified_concepts_long_sentence]  

    return document
 
def line_cleansing(sentence):

    if (sentence == None) or (sentence == ""):
        return ""
    
    word_count = 0
    
    # eliminate char and numbers
    sentence = clean_sentence_noise(sentence)
    
    # stoplist words                                 
    sentence, sentence_temp = stoplist(trim(sentence))
    
    # Word size constraint
    word_count = len(sentence_temp.split())
        
    if (word_count<=MIN_KEYWORD_LEN):    
        if (len(sentence_temp)>MAX_KEYWORD_LEN) or (len(sentence_temp)<=MIN_KEYWORD_LEN):
            save_noise(sentence_temp)

    if (sentence == None) or (sentence == ""):
        return "", ""
    
    if (sentence_temp == None) or (sentence_temp == ""):
        return "", ""
    
    # special text processing for lower case text 
    sentence_temp = sentence_temp.replace("\n", "")
    sentence = sentence.replace("\n", "")  
    
    # string cleansing
    sentence_temp = trim(sentence_temp)
    sentence = trim(sentence)   
    
    if (sentence == None) or (sentence == ""):
        return "", ""
    
    if (sentence_temp == None) or (sentence_temp == ""):
        return "", ""
    
    # output to user program flow
    #print("sentence_temp: " + sentence_temp)
    #print("sentence: " + sentence)
    
    # final string cleansing
    sentence_temp = trim(sentence_temp)
    sentence = trim(sentence)
    
    return sentence, sentence_temp
   
def clean_wiki_noise_from_line(line):        
    # preformating word     
    line = trim(line)
    line_clean = line.lower() 

    if (line_clean=="") or (line_clean==" "): 
        return ""

    with open("stoplist.txt","r") as file: 
        # reading each line"
        for sentence in file:
            
            sentence = sentence.replace("\n","")
            sentence = trim(sentence.lower())
            
            line_clean = line_clean.replace("\n","")
            line_clean = trim(line_clean)
             
            if line_clean in sentence:
                #print("CLEANING AND ELIMINATING SENTENCE")
                return ""
                
    return line

def check_line_stop_sentences(temp_line):
    
    #PATH = "/home/dr-g/Projet/Programmation/Python/wiki-AI/"
    #files = os.listdir(PATH)
    #relax(RELAX_TIME)
    
    with open("stop_sentences.txt","r") as file: 
        # reading each line"
        for sentence in file:
            sentence, temp_line = normalize(sentence.lower(), temp_line) 
            #print("loaded sentence:        \t\t" + sentence)
            #print("line being verified:    \t\t" + temp_line)
            if sentence in temp_line:
                #limit = int(len(temp_line)/4)
                #print("We have a match for:         \t\t" + temp_line[0:limit])
                #print("loaded stop sentence:        \t\t" + sentence)
                return " "
    return temp_line

def check_line_for_stop_code(temp_line):
    
    #PATH = "/home/dr-g/Projet/Programmation/Python/wiki-AI/"
    #files = os.listdir(PATH)
    #relax(RELAX_TIME)

    with open("stop_code.txt","r") as file: 
        # reading each line"
        for sentence in file:
            sentence, temp_line = normalize(sentence.lower(), temp_line) 
            #print("loaded sentence:        \t\t" + sentence)
            #print("line being verified:    \t\t" + temp_line)
            if sentence in temp_line:
                limit = int(len(temp_line)/4)
                #print("We have a match for:         \t\t" + temp_line[0:limit])
                #print("loaded code stop sentence:    \t\t" + sentence)
                return " "
    return temp_line

def normalize(first_match, second_match):
    first_match = first_match.replace("\n", "") 
    second_match = second_match.replace("\n", "") 
    return first_match, second_match

def stoplist(word):
    # clean common word
    # NOISE ELIMINATION   
    word = trim(word)
    word_temp = word.lower()
    
    for word_verifier in word_temp.split():
        
        if (word_verifier=="") or (word_verifier==" "): 
            continue
        
        with open("/home/dr-g/Projet/Programmation/Python/wiki-nerd/stoplist.txt","r") as file: 
            # reading each line"
            for sentence in file:
                
                sentence = sentence.replace("\n","")
                sentence = trim(sentence)
                
                word_verifier = trim(word_verifier)
                
                
                if (word_verifier == sentence):
                    if len(word_temp.split()) > 1:
                        word_verifier = word_verifier + " "
                        word_temp = word_temp.replace(word_verifier, "")
                    else:
                        word_temp = word_temp.replace(word_verifier, "")
                    break
                    
            file.close()
              
    return word, word_temp

def clean_sentence_noise(line):
    
    line = trim(line)
    index = 0
    
    for word in line:
        for char in word:
            if not char in "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789áÁàÀâÂäÄãÃåÅæÆçéÉèÈêëËÍìÌîÎïÏñÑóÓòÒôÔöÖõÕøØœŒßúÚùÙûÛüÜ":                    
                word = word.replace(char, " ")
            
            if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                
                previous_letter = ''
                
                if (index-1>=0):
                    previous_letter = word[index-1]
                
                if (previous_letter.islower()):
                    word = word.replace(char, " " + char)
 
            if char in "^\"\'()?\\/$*":
                word = word.replace(char, " ")

            index = index + 1
        index = 0
    line = trim(line)
    return line

def clean_word_noise(word):    
    for char in word:
        if not char in "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789áÁàÀâÂäÄãÃåÅæÆçéÉèÈêëËÍìÌîÎïÏñÑóÓòÒôÔöÖõÕøØœŒßúÚùÙûÛüÜ":                    
            word = word.replace(char, " ")
    word = trim(word)
    return word

def clean_word_seperation(word):
    index = 0
    for char in word:
        if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            previous_letter = ''
            if (index-1>0):
                previous_letter = word[index-1]
            if (previous_letter.islower()):
                word = word.replace(char, " " + char)
        index = index + 1
    word = trim(word)
    return word

def clean_word_final(word):
    index = 0
    for char in word:
        # ^ is the references char
        if char in "()(){},:;|*/+\"\\~^–":
            word = word.replace(char, " ")
        index = index + 1
    
    word = trim(word)
    return word

# Function used in MATCH PHASE 
def clean_month(word):   
    word = trim(word)
    
    word = word.replace("january"," ")
    word = word.replace("february"," ")
    word = word.replace("march"," ")
    word = word.replace("april"," ")
    word = word.replace("may"," ")
    word = word.replace("june"," ")
    word = word.replace("july"," ")
    word = word.replace("august"," ")
    word = word.replace("september"," ")
    word = word.replace("october"," ")
    word = word.replace("november"," ")
    word = word.replace("december"," ")
    
    word = word.replace("January"," ")
    word = word.replace("February"," ")
    word = word.replace("March"," ")
    word = word.replace("April"," ")
    word = word.replace("May"," ")
    word = word.replace("June"," ")
    word = word.replace("July"," ")
    word = word.replace("August"," ")
    word = word.replace("September"," ")
    word = word.replace("October"," ")
    word = word.replace("November"," ")
    word = word.replace("December"," ")
    
    word = word.replace("JANUARY"," ")
    word = word.replace("FEBRUARY"," ")
    word = word.replace("MARCH"," ")
    word = word.replace("APRIL"," ")
    word = word.replace("MAY"," ")
    word = word.replace("JUNE"," ")
    word = word.replace("JULY"," ")
    word = word.replace("AUGUST"," ")
    word = word.replace("SEPTEMBER"," ")
    word = word.replace("OCTOBER"," ")
    word = word.replace("NOVEMBER"," ")
    word = word.replace("DECEMBER"," ")
            
    word = trim(word)
    
    return word    

def trim(text_section): 
    text_section = text_section.strip()
    text_section = text_section.lstrip()
    return text_section 

def relax(sec):
    time.sleep(sec) 
    
def save_noise(noise):
    f = open("noise.txt", "a")
    f.write("\n" + str(noise))
    f.write("\n")
    f.close

# start the program
start_program()