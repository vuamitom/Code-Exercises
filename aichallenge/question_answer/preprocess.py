import json
import csv
import string
from utils import tokenize_sentence
from relevance import rel_ranking

def para_to_sentences(text):
    return tokenize_sentence(text)

def main():
    content = None
    with open('./raw/train.json') as f:
        content = f.read()
    data = json.loads(content)
    for q in data:
        sentences = para_to_sentences(q['text'])        
        if q['label'] is True:
            # rank sentence to find the right one
            if len(sentences) == 1:
                sentences = [(sen, 1) for sen in sentences]
            else:
                # do scoring
                sentences = rel_score(q['question'], sentences)
        else:
            sentences = [(sen, 0) for sen in sentences]
        q['sentences'] = sentences

    with open('./data/train.tsv', 'w') as f:
        writer = csv.write(f, delimiter='\t')
        for q in data:
            for sen in q['sentences']:
                # writer.write(())
                pass

if __name__ == '__main__':
    main()

