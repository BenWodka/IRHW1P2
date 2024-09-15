import sys
import spacy
import re
import os
import html

def strip(text):

    cleanText = html.unescape(text)

    tagPattern = r'(?<=\b(?:alt|content)=["\'])([^"\']+)(?=["\'])'
    tagMatches = re.findall(tagPattern, cleanText)

    cleanText = re.sub(r'<.*?>', '', cleanText)
    cleanText = re.sub(r'\s+', ' ', cleanText).strip().lower()

    cleanText += ' ' + ' '.join(tagMatches)

    return cleanText

 
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

    doc = nlp(text)
    tokens = [token.text for token in doc if token.text.isdigit() or token.is_alpha()]

    tokens.extend(urls)
    tokens.extend(emails)

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
