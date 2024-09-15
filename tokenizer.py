import nltk
import sys
import spacy
import re
import os
import html

def strip(text):

    clean_text = html.unescape(text)
    clean_text = re.sub(r'<.*?>', '', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip().lower()
    return clean_text

 
def removeFileExtension(inputpathname):

    root, ext = os.path.splitext(inputpathname)
    return root

def getTokens(doc):

    final = ""
    for token in doc:
        final += str(token) + "\n"  
    return final.strip()

def processFile(filename, nlp):

    with open(filename, 'r') as f:
        s = f.read()
        s = strip(s)
    return tokenize(s, nlp)

def tokenize(text, nlp):

    doc = nlp(text)
    tokens = [token.text for token in doc]
    return tokens

def main(inputDirectory, outputDirectory):

    nlp = spacy.blank("en")
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    for filename in os.listdir(inputDirectory):
        fullPath = os.path.join(inputDirectory, filename)
        tokens = processFile(fullPath, nlp)
        outputFile = os.path.join(outputDirectory, removeFileExtension(filename))
        with open(f"{outputFile}.txt", "w") as write:
            write.write('\n'.join(tokens) + '\n')

 

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Program needs input directory and output directory")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
