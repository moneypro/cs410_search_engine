import sys, argparse
from string import ascii_lowercase, whitespace, punctuation
from lowercase_tok import tokens_lowercase

p = argparse.ArgumentParser()
p.add_argument("file")
p.add_argument("-s", "--size")
p.add_argument("-o", "--output")

args = p.parse_args()
# print (Namespace)
size = int(args.size)
outLines = ""

with open(args.file) as f:
	content = f.readlines()
	for i in range(0, min(len(content), 2*size), 2):
		line = (content[i].strip() + ' ' + content[i+1].strip())
		line = tokens_lowercase(line)
		# line = ''.join([c for c in line if c in ascii_lowercase + ' ']).translate(str.maketrans(whitespace + punctuation, ' '*len(whitespace+punctuation)))
		outLines += line + '\n'

with open(args.output, 'w') as f:
	f.write(outLines)
