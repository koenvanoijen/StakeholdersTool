import spacy
from collections import Counter
from spacy import displacy
nlp = spacy.load('en_core_web_sm')
nlp_nl = spacy.load('nl_core_news_sm')
def tagging(text, dutch):
    print(text)
    if dutch:
        textNLP = nlp_nl(text)
    else:
        textNLP = nlp(text)
    print([(X.text, X.label_) for X in textNLP.ents if X.label_ == 'PERSON' or X.label_ == 'ORG'])
    return textNLP