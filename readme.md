# CS 410 Final Project Submission

## Python scripts
* lowercase_tok.py: metapy tokenizer integrated from mp1. helper for tokenizing inputs.
* parser.py: parse the raw file from DBLP into a text file where each line represents a document. Each line is the concatenation of title and abstract. `python parser.py raw_text.txt -s size -o parsed_input.txt`
* plsa2.py: main algorithm of plsa. Construct the model with inputs where each line is a document. It saves the model in a pkl file. `python plsa2.py parsed_input.txt`
* school_author.py: find the most frequent authors group by schools.
* search.py: search with given input. It can also takes only titles for fancier printing. `python search.py parsed_input.txt query [parsed_input_titles_only.txt]`.
* title_author_parser.py: find the collaborator for a given author.

## Web
Usage: Run on a localhost or deploy on a server with node.js. My configuration is JetBrains WebStorm Student License on Windows 10 X64. 
