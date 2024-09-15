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

if compgen -G "*.txt" > /dev/null; then
    cat *.txt > combinedTokens.txt
fi

sort combinedTokens.txt | uniq -c | sort -k2 > tempalpha.txt
sort combinedTokens.txt | uniq -c | sort -nr > tempfreqs.txt

awk '{print $2, $1}' tempalpha.txt > alpha.txt
awk '{print $2, $1}' tempfreqs.txt > freqs.txt

rm tempalpha.txt tempfreqs.txt 