#!/bin/bash

inputDirectory="$1"
outputDirectory="$2"

if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_dir> <output_dir>"
    exit 1
fi

echo '----compiling'
python3 tokenizer.py "$inputDirectory" "$outputDirectory"
echo '----running'

cd "$outputDirectory"

find . -type f -name "*.txt" ! -name "combinedTokens.txt" -exec cat {} + > combinedTokens.txt

if [ ! -f combinedTokens.txt ]; then
    echo "combinedTokens.txt could not be created."
    exit 1
fi

sort combinedTokens.txt | uniq -c | sort -k2 > tempalpha.txt
sort combinedTokens.txt | uniq -c | sort -nr > tempfreqs.txt

cd ..

awk '{print $2, $1}' "$outputDirectory/tempalpha.txt" > alpha.txt
awk '{print $2, $1}' "$outputDirectory/tempfreqs.txt" > freqs.txt

rm tempalpha.txt tempfreqs.txt 