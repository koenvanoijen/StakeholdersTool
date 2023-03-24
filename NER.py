from flair.models import SequenceTagger
from flair.data import Sentence


###based on model from https://huggingface.co/flair/ner-dutch-large #####
### With flair we have the posibility to train ourselves on data, but for now it works fine.
def predictPerson(text):
    tagger = SequenceTagger.load("flair/ner-dutch-large")

    # make example sentence
    sentence = Sentence(text)

    # predict NER tags
    tagger.predict(sentence)

    # print sentence
    # print(sentence)

    # print predicted NER spans
    print('The following NER tags are found:')
    # iterate over entities and print
    for entity in sentence.get_spans('ner'):
        print(entity)
    print('....')
    print('All persons on this website are')
    for entity in sentence.get_labels():
        if entity.value == 'PER':
            print(entity)

    