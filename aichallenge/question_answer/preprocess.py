import json
import csv
import string
from utils import tokenize_sentence
from relevance import rel_ranking
from transformers import BertTokenizer
import math
# from underthesea import word_tokenize
MAX_SEQ_LENGTH = 128

def dummy_split(text, ratio):    
    # uwords = word_tokenize(q['text'])
    dummy = text.split(' ')
    steps = math.ceil(len(dummy)/ratio)
    r = []
    for i in range(0, ratio):
        r.append(' '.join(dummy[i*steps:((i*steps) + steps) if i < (ratio - 1) else len(dummy)]))
    return r

def new_main():
    content = None
    with open('./raw/train.json') as f:
        content = f.read()
    data = json.loads(content)
    countd, countm = 0, 0
    ml = 0

    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', cache_dir='./models', do_lower_case=False)
    for q in data:
        words = tokenizer.tokenize(q['text'])        
        ml = len(words) if len(words) > ml else ml
        if len(words) > MAX_SEQ_LENGTH:
            sentences = tokenize_sentence(q['text'])
            sentences = [s for s in sentences if len(s) > 3]
            if len(sentences) < 2:
                # can't tokenize 
                # do smth stupid instead 
                ratio = math.ceil(len(words) * 1.0 / MAX_SEQ_LENGTH)
                # uwords = word_tokenize(q['text'])
                # dummy = q['text'].split(' ')
                # steps = math.ceil(len(dummy)/ratio)
                # r = []
                # for i in range(0, ratio):
                #     r.append(' '.join(dummy[i*steps:((i*steps) + steps) if i < (ratio - 1) else len(dummy)]))
                sentences = dummy_split(q['text'], ratio);

            if q['label'] is True:
                # rank                
                sentences = rel_ranking(q['question'], sentences)                                                      
                relcount = sum([1 if v[0] > 0 else 0 for v in sentences])
                delta = sentences[0][0] - sentences[1][0]
                if relcount == 1 or delta > 4:
                    q['sentences'] = [(v[1], 1 if idx == 0 else 0) for idx, v in enumerate(sentences)]
                else:
                    if len(tokenizer.tokenize(sentences[0][1] + ' . ' + sentences[1][1])) < MAX_SEQ_LENGTH:
                        q['sentences'] = [(sentences[0][1] + ' . ' + sentences[1][1], 1)]
                        q['sentences'] += [(s[1], 0) for s in sentences[2:]]
                    else:
                        # accept the risk 
                        q['sentences'] = [(v[1], 1 if idx == 0 else 0) for idx, v in enumerate(sentences)]
            else:
                q['sentences'] = [(sen, 0) for sen in sentences]
                                
    with open('./data/train.tsv', 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(('id', 'q_id', 'ans_id', 'question', 'answer', 'is_correct'))
        for idx, q in enumerate(data):
            if 'sentences' in q:
                q_id = q['id']
                for aidx, sen in enumerate(q['sentences']):
                    # writer.write(())
                    txt, is_correct = sen
                    ans_id = q_id + '_ans_' + str(aidx)
                    writer.writerow((str(idx), q_id, ans_id, q['question'], txt.replace('\t', ' '), str(is_correct)))                    
            else:
                is_correct = 1 if q['label'] else 0
                q_id = q['id']
                ans_id = q_id + '_ans_0'
                writer.writerow((str(idx), q_id, ans_id, q['question'], q['text'].replace('\t', ' '), str(is_correct)))

def preprocess_test():
    content = None
    with open('./raw/test.json') as f:
        content = f.read()
    data = json.loads(content)
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', cache_dir='./models', do_lower_case=False)
    rows = []
    for q in data:
        for p in q['paragraphs']:
            words = tokenizer.tokenize(p['text'])
            if len(words) > MAX_SEQ_LENGTH:
                sentences = tokenize_sentence(p['text'])
                sentences = [s for s in sentences if len(s) > 3]
                if len(sentences) < 2:
                    # can't tokenize 
                    # do smth stupid instead 
                    ratio = math.ceil(len(words) * 1.0 / MAX_SEQ_LENGTH)                    
                    sentences = dummy_split(p['text'], ratio);

                for idx, sen in enumerate(sentences):
                    rows.append((q['__id__'], p['id'] + '$$' + str(idx), q['question'], sen))
            else:
                rows.append((q['__id__'], p['id'], q['question'], p['text']))
    with open('./data/dev.tsv', 'w') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerow(('id', 'q_id', 'ans_id', 'question', 'answer', 'is_correct'))
        for idx, row in enumerate(rows):
            q_id, ans_id, question, ans = row 
            writer.writerow((str(idx), q_id, ans_id, question, ans.replace('\t', ' '), 0))

def gather_answer():
    is_corrects = None
    with open('pred_results.txt', 'r') as f:
        is_corrects = f.readlines()
    is_corrects = [int(x) for x in is_corrects]
    results = []
    with open('./data/dev.tsv', 'r') as f:
        reader = csv.reader(f, delimiter = '\t')
        for idx, r in enumerate(reader):
            if idx == 0:
                continue
            _, q_id, ans_id, question, answer, _ = r
            is_correct = is_corrects[idx-1]
            if is_correct == 1:
                if ans_id.find('$$') >= 0:
                    print('????---> ', question)
                    print(answer)
                    para_id = ans_id.split('$$')[0]
                    if len(results) > 0:                        
                        prev = results[-1]                        
                        prev_qid, prev_pid = prev
                        if prev_qid == q_id and prev_pid == para_id:
                            # already added 
                            continue
                        else:
                            results.append((q_id, para_id))
                else:
                    results.append((q_id, ans_id))
    with open('submission.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(('test_id', 'answer'))
        for r in results:
            writer.writerow(r)


if __name__ == '__main__':
    # test
    new_main()
