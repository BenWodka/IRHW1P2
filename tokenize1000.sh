#!/bin/bash

inputDirectory="$1"
outputDirectory="$2"

n=1000
if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_dir> <output_dir>"
    exit 1
fi

echo '----compiling'

# Create a temporary directory to hold the first n files
tempInputDir=$(mktemp -d)

find "$inputDirectory" -type f -name "*.html" | head -n "$n" | xargs -I {} cp {} "$tempInputDir"

if [ "$(ls -A $tempInputDir)" ]; then
    # Pass the temporary input directory to the Python script
    python3 tokenizer.py "$tempInputDir" "$outputDirectory"
else
    echo "No files found to process in the input directory."
    exit 1
fi

echo '----running'

cd "$outputDirectory"

find . -type f -name "*.txt" ! -name "combinedTokens.txt" | xargs cat > combinedTokens.txt

if [ ! -f combinedTokens.txt ]; then
    echo "combinedTokens.txt could not be created."
    exit 1
fi

sort combinedTokens.txt | uniq -c | sort -k2 > tempalpha.txt
sort combinedTokens.txt | uniq -c | sort -nr > tempfreqs.txt

cd ..

awk '{print $2, $1}' "$outputDirectory/tempalpha.txt" > "alpha$n.txt"
awk '{print $2, $1}' "$outputDirectory/tempfreqs.txt" > "freqs$n.txt"

rm "$outputDirectory/tempalpha.txt" "$outputDirectory/tempfreqs.txt"
rm -rf "$tempInputDir"