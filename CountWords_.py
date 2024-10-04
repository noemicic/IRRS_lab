import sys
import re
from spellchecker import SpellChecker
import chardet

spell = SpellChecker(language="en")  

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  
    result = chardet.detect(raw_data)
    return result['encoding']


def is_word(word):
    if re.match(r'\b\d+\b', word):  # numbers
        return False
    if re.match(r'https?://\S+|www\.\S+', word):  # URL
        return False
    if len(word) < 2:  # Parole troppo corte
        return False
    return word in spell

#Main def
def process_file(input_file, output_file):
    valid_words = []
    
    encoding = detect_encoding(input_file)

    #Input file
    with open(input_file, newline='', encoding=encoding) as infile:
        for line in infile:
            parts = line.split(", ")  
            if len(parts) == 2:
                count, word = parts
                word = word.strip().lower()  
                # Filtriamo solo le parole corrette
                if is_word(word):
                    valid_words.append((int(count), word))
    
    #Sorting the words lexicographically
    valid_words.sort( key=lambda x: (-x[0], x[1]))
    
    #Output file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        for count, word in valid_words:
            outfile.write(f"{count} {word}\n")

input_file=sys.argv[1]
output_file=sys.argv[2]
process_file(input_file,output_file)


