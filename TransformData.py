import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
#nltk.download('stopwords')
def tokenize(text):
    return wordpunct_tokenize(text)

def stopWordRemoval(text):
    stop_words = set(stopwords.words('dutch') + stopwords.words('english') + ['wij'])
    # converts the words in word_tokens to lower case and then checks whether
    # they are present in stop_words or not
    return [w for w in text if not w.lower() in stop_words]

def preproccess(text):
    tText = tokenize(text)
    filtered_text = stopWordRemoval(tText)
    #print(stopwords.words('dutch'))
    print(filtered_text)

