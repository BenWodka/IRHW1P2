import resource
import sys
import spacy
import re
import os
import html
import time

#Strip HTML tags and special characters
def strip(text):

    #Unescape HTML
    cleanText = html.unescape(text)

    #Pattern to match 'alt' and 'content'  HTML attributes
    tagPattern = r'\b(?:alt|content)=["\']([^"\']+)(?=["\'])'
    tagMatches = re.findall(tagPattern, cleanText)

    #Removes HTML tags and extra whitespace, and converts to lowercase
    cleanText = re.sub(r'<.*?>', '', cleanText)
    cleanText = re.sub(r'\s+', ' ', cleanText).strip().lower()

    cleanText += ' ' + ' '.join(tagMatches)

    return cleanText

#Removes file extensions
def removeFileExtension(inputpathname):

    root, ext = os.path.splitext(inputpathname)
    return root

#Converts document into tokens separated by newline
def getTokens(doc):

    final = ""
    for token in doc:
        final += str(token) + "\n"  
    return final.strip()

#Reads content, strips it, and tokenizes it
def processFile(filename, nlp):

    with open(filename, 'r') as f:
        s = f.read()
        s = strip(s)
    return tokenize(s, nlp)

#Tokenizes using regex patterns
def tokenize(text, nlp):

    #removing unwanted elements
    urlPattern = re.compile(r'http[s]?://\S+')
    emailPattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    floatingPointPattern = re.compile(r'\b\d+\.\d+\b')
    punctuationPattern = re.compile(r'[^\w\s]')

    #detect urls and emails
    urls = urlPattern.findall(text)
    emails = emailPattern.findall(text)

    # remove unwanted elements
    text = urlPattern.sub('', text)
    text = emailPattern.sub('', text)
    text = floatingPointPattern.sub('', text)
    text = punctuationPattern.sub('', text)

    #tokenize the cleaned text
    doc = nlp(text)
    tokens = [token.text for token in doc if token.is_alpha]

    tokens.extend(urls)
    tokens.extend(emails)

    return tokens

#Main, processes files from inputDirectory to outputDirectory
def main(inputDirectory, outputDirectory):


    nlp = spacy.blank("en")
    nlp.max_length = 2000000 #increase memory allocation, necessary for VS Code and maybe Turing

    #if outputDirectory of given name doesn't exist, make it
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    #Process files in inputDirectory
    for filename in os.listdir(inputDirectory):
        fullPath = os.path.join(inputDirectory, filename)
        if os.path.isfile(fullPath):
            tokens = processFile(fullPath, nlp)
            outputFile = os.path.join(outputDirectory, removeFileExtension(filename))
            with open(f"{outputFile}.txt", "w") as write:
                write.write('\n'.join(tokens) + '\n')

 

if __name__ == '__main__':
    if len(sys.argv) != 3: #only 2 arguments allowed
        print("Program needs input directory and output directory")
        sys.exit(1)

    startRealTime = time.time()  # Real time
    startUserTime = resource.getrusage(resource.RUSAGE_SELF).ru_utime  # User time

    # Call main with given arguments
    main(sys.argv[1], sys.argv[2])

    # End time measurement
    endRealTime = time.time()
    endUserTime = resource.getrusage(resource.RUSAGE_SELF).ru_utime

    elapsedRealTime = endRealTime - startRealTime
    elapsedUserTime = endUserTime - startUserTime

    print(f"Real time: {elapsedRealTime:.2f} seconds")
    print(f"User time (CPU): {elapsedUserTime:.2f} seconds")
