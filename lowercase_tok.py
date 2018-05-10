import metapy

def tokens_lowercase(string):
    #Write a token stream that tokenizes with ICUTokenizer, 
    #lowercases, removes words with less than 2 and more than 5  characters
    #performs stemming and creates trigrams (name the final call to ana.analyze as "trigrams")
    '''Place your code here'''
    doc = metapy.index.Document()
    doc.content(string)
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.LowercaseFilter(tok)
    tok = metapy.analyzers.LengthFilter(tok, min=2, max=20)
    tok = metapy.analyzers.Porter2Filter(tok)
    ana = metapy.analyzers.NGramWordAnalyzer(1, tok)
    trigrams = ana.analyze(doc)

    #leave the rest of the code as is
    tok.set_content(doc.content())
    tokens, counts = [], []
    for token, count in trigrams.items():
        counts.append(count)
        tokens.append(token)
    return ' '.join(tokens)
    
if __name__ == '__main__':
    # print(doc.content()) #you can access the document string with .content()
    tokens = tokens_lowercase("I said that I can't believe that it only costs $19.95! I could only find it for more than $30 before.")
    print(tokens)
