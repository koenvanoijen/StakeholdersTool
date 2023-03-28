import spacy
from collections import Counter
from spacy import displacy
nlp = spacy.load('en_core_web_sm')
nlp_nl = spacy.load('nl_core_news_sm')

#### This file is the spacy text analyis including capRecognition that still doesn't work.

##### In other words: could be removed in the near future ######
def taggingSPACY(text, dutch):
    if dutch:
        textNLP = nlp_nl(text)
    else:
        textNLP = nlp(text)
    print([(X.text, X.label_) for X in textNLP.ents if X.label_ == 'PERSON' or X.label_ == 'ORG'])
    items = [x.text for x in textNLP.ents if x.label_ == 'PERSON']
    print(Counter(items).most_common(3))
    return textNLP


#Far from foolproof and does not work as I wanted to it 
def capRecognition(text):
    # Look for every word starting with Caps
    capWords = []
    print(text)
    i = 0
    while i < len(text):
        if text[i][0].isupper():
            capWords.append(text[i])
            while text[i+1][0].isupper() or text[i+1] in ["de", "van", "'"]:
                capWords[-1] = capWords[-1] + " " + text[i+1]
                if i < len(text) -1:
                    i = i + 1
        i = i + 1
    for i, t in enumerate(capWords):
        if len(t) > 2:
            if t[-3] == 'v' and t[-2] == 'a' and t[-1] == 'n':
                capWords[i] = t.replace('van', '')
            if t[-2] == 'd' and t[-1] == 'e':
                capWords[i] = t.replace(' de', '')
    print(capWords)
    capWords.sort(key=len, reverse=True)
    for i, c in enumerate(capWords):
        k = i
        while k != 0:
            if c.lower() in capWords[k-1].lower():
                capWords[i] = capWords[k-1]
                break
            k = k - 1
    print(Counter(capWords))
    print("https://unbiased-coder.com/extract-names-python-nltk/")

