import json
import csv
import string
from utils import tokenize_sentence
from relevance import rel_ranking
from transformers import BertTokenizer, XLNetTokenizer
import underthesea
import math
from random import shuffle
# from underthesea import word_tokenize
MAX_SEQ_LENGTH = 128

def sanitize(s):
    return s.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')

def dummy_split(text, ratio):    
    # uwords = word_tokenize(q['text'])
    dummy = text.split(' ')
    steps = math.ceil(len(dummy)/ratio)
    r = []
    for i in range(0, ratio):
        r.append(' '.join(dummy[i*steps:((i*steps) + steps) if i < (ratio - 1) else len(dummy)]))
    return r

def new_main(model_type='bert'):
    content = None
    with open('./raw/all_train.json') as f:
        content = f.read()
    data = json.loads(content)
    countd, countm = 0, 0
    ml = 0

    if True:
        with open('./raw/masked_train.json') as f:
            content = f.read()
            data += json.loads(content)
    tokenizer = None
    if model_type == 'bert':
        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', cache_dir='./models', do_lower_case=False)
    else:
        tokenizer = XLNetTokenizer.from_pretrained('xlnet-base-cased', cache_dir='./models', do_lower_case=False)
    for q in data:
        # if not q['id'] == 'u4-1551859077_0': continue
        words = tokenizer.tokenize(q['text'])        
        ml = len(words) if len(words) > ml else ml
        if len(words) > MAX_SEQ_LENGTH:
            sentences = tokenize_sentence(q['text'])
            sentences = [s for s in sentences if len(s) > 3]
            if len(sentences) < 2:                
                ratio = math.ceil(len(words) * 1.0 / MAX_SEQ_LENGTH)                
                sentences = dummy_split(q['text'], ratio);

            if q['label'] is True:
                # rank                
                sentences = rel_ranking(q['question'], sentences)                                                      
                relcount = sum([1 if v[0] > 0 else 0 for v in sentences])
                delta = sentences[0][0] - sentences[1][0]
                if relcount == 1:
                    q['sentences'] = [(v[1], 1 if idx == 0 else 0) for idx, v in enumerate(sentences)]                    
                else:
                    idx = 0
                    chosen = ''
                    while len(tokenizer.tokenize(chosen + (' . ' if len(chosen) > 0 else '') + sentences[idx][1])) < MAX_SEQ_LENGTH:
                        chosen = chosen + (' . ' if len(chosen) > 0 else '') + sentences[idx][1]
                        idx += 1                    
                    q['sentences'] = [(chosen, 1)]
                    q['sentences'] += [(s[1], 0) for s in sentences[idx:]]
            else:
                q['sentences'] = [(sen, 0) for sen in sentences]

    # if True:
    #     print('---- count = ', countd)
    #     return                                
    with open('./data/bert_train.tsv', 'w') as f:
        writer = csv.writer(f, delimiter='\t', quotechar=None)
        writer.writerow(('id', 'q_id', 'ans_id', 'question', 'answer', 'is_correct'))
        for idx, q in enumerate(data):
            if 'sentences' in q:
                q_id = q['id']
                for aidx, sen in enumerate(q['sentences']):
                    # writer.write(())
                    txt, is_correct = sen
                    ans_id = q_id + '_ans_' + str(aidx)
                    writer.writerow((str(idx), q_id, ans_id, sanitize(q['question']), sanitize(txt), str(is_correct)))                    
            else:
                is_correct = 1 if q['label'] else 0
                q_id = q['id']
                ans_id = q_id + '_ans_0'
                print(q['question'])
                print(q['text'])
                writer.writerow((str(idx), q_id, ans_id, sanitize(q['question']), sanitize(q['text']), str(is_correct)))

# def new_main_2():
#     content = None
#     with open('./raw/train.json') as f:
#         content = f.read()
#     data = json.loads(content)
#     countd, countm = 0, 0
#     ml = 0

#     tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', cache_dir='./models', do_lower_case=False)
#     for q in data:
#         # if not q['id'] == 'u3-1557287872_0': continue
#         words = tokenizer.tokenize(q['title'] + ' . ' + q['text'])        
#         ml = len(words) if len(words) > ml else ml
#         if len(words) > MAX_SEQ_LENGTH:
#             sentences = tokenize_sentence(q['text'])
#             # print('----------', sentences)
#             sentences = [s for s in sentences if len(s) > 3]
#             if len(sentences) < 2:                
#                 ratio = math.ceil(len(words) * 1.0 / MAX_SEQ_LENGTH)                
#                 sentences = dummy_split(q['text'], ratio);
#             if q['label'] is True:
#                 # rank                
#                 sentences = rel_ranking(q['question'], sentences)                                                      
#                 relcount = sum([1 if v[0] > 0 else 0 for v in sentences])
#                 delta = sentences[0][0] - sentences[1][0]
#                 if relcount == 1:
#                     q['sentences'] = [(q['title'] + ' . ' + v[1], 1 if idx == 0 else 0) for idx, v in enumerate(sentences)]                    
#                 else:
#                     idx = 0
#                     chosen = q['title']
#                     while len(tokenizer.tokenize(chosen + ' . ' + sentences[idx][1])) < MAX_SEQ_LENGTH:
#                         chosen =  chosen + ' . ' + sentences[idx][1]
#                         idx += 1                    

#                     if idx == 0:
#                         chosen = q['title'] + sentences[0][1]
#                         idx = 1
#                         # let BERT do the work
#                     q['sentences'] = [(chosen, 1)]
#                     q['sentences'] += [(q['title'] + ' . ' + s[1], 0) for s in sentences[idx:]]
#             else:
#                 q['sentences'] = [(q['title'] + ' . ' + sen, 0) for sen in sentences]
#         else:
#             q['text'] = q['title'] + ' . ' + q['text']
#         # print(q )
#         # return 
#     with open('./data/train_with_title.tsv', 'w') as f:
#         writer = csv.writer(f, delimiter='\t')
#         writer.writerow(('id', 'q_id', 'ans_id', 'question', 'answer', 'is_correct'))
#         for idx, q in enumerate(data):
#             if 'sentences' in q:
#                 q_id = q['id']
#                 for aidx, sen in enumerate(q['sentences']):
#                     # writer.write(())
#                     txt, is_correct = sen
#                     ans_id = q_id + '_ans_' + str(aidx)
#                     writer.writerow((str(idx), q_id, ans_id, q['question'], txt.replace('\t', ' '), str(is_correct)))                    
#             else:
#                 is_correct = 1 if q['label'] else 0
#                 q_id = q['id']
#                 ans_id = q_id + '_ans_0'
#                 writer.writerow((str(idx), q_id, ans_id, q['question'], q['text'].replace('\t', ' '), str(is_correct)))


def preprocess_test(model_type='bert'):
    content = None
    with open('./raw/test.json') as f:
        content = f.read()
    data = json.loads(content)
    tokenizer = None
    if model_type == 'bert':
        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', cache_dir='./models', do_lower_case=False)
    else:
        tokenizer = XLNetTokenizer.from_pretrained('xlnet-base-cased', cache_dir='./models', do_lower_case=False)
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
        writer = csv.writer(f, delimiter = '\t', quotechar=None)
        writer.writerow(('id', 'q_id', 'ans_id', 'question', 'answer', 'is_correct'))
        for idx, row in enumerate(rows):
            q_id, ans_id, question, ans = row 
            writer.writerow((str(idx), q_id, ans_id, sanitize(question), sanitize(ans), 0))

# def preprocess_test_2():
#     content = None
#     with open('./raw/test.json') as f:
#         content = f.read()
#     data = json.loads(content)
#     tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', cache_dir='./models', do_lower_case=False)
#     rows = []
#     for q in data:
#         for p in q['paragraphs']:
#             words = tokenizer.tokenize(q['title'] + ' . ' + p['text'])
#             if len(words) > MAX_SEQ_LENGTH:
#                 sentences = tokenize_sentence(p['text'])
#                 sentences = [s for s in sentences if len(s) > 3]
#                 if len(sentences) < 2:
#                     # can't tokenize 
#                     # do smth stupid instead 
#                     ratio = math.ceil(len(words) * 1.0 / MAX_SEQ_LENGTH)                    
#                     sentences = dummy_split(p['text'], ratio);

#                 for idx, sen in enumerate(sentences):
#                     rows.append((q['__id__'], p['id'] + '$$' + str(idx), q['question'], q['title'] + ' . '  + sen))
#             else:
#                 rows.append((q['__id__'], p['id'], q['question'], q['title'] + ' . ' +  p['text']))
#     with open('./data/dev_with_title.tsv', 'w') as f:
#         writer = csv.writer(f, delimiter = '\t')
#         writer.writerow(('id', 'q_id', 'ans_id', 'question', 'answer', 'is_correct'))
#         for idx, row in enumerate(rows):
#             q_id, ans_id, question, ans = row 
#             writer.writerow((str(idx), q_id, ans_id, question, ans.replace('\t', ' '), 0))
# def preprocess_test_2():
#     content = None
#     with open('./raw/test.json') as f:
#         content = f.read()
#     data = json.loads(content)
#     tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', cache_dir='./models', do_lower_case=False)
#     rows = []
#     count = 0
#     for q in data:
#         for p in q['paragraphs']:
#             words = tokenizer.tokenize(p['text'])
#             if len(words) > MAX_SEQ_LENGTH:
#                 sentences = tokenize_sentence(p['text'])
#                 sentences = [s for s in sentences if len(s) > 3]
#                 if len(sentences) < 2:
#                     # can't tokenize 
#                     # do smth stupid instead 
#                     ratio = math.ceil(len(words) * 1.0 / MAX_SEQ_LENGTH)                    
#                     sentences = dummy_split(p['text'], ratio);

#                 for idx, sen in enumerate(sentences):
#                     # join sentence instead of just truncating here
#                     if idx < (len(sentences) - 1) and \
#                         len(tokenizer.tokenize(sen + ' . ' +  sentences[idx + 1])) < MAX_SEQ_LENGTH:
#                         count += 1
#                         rows.append((q['__id__'], p['id'] + '$$' + str(idx), q['question'], sen + ' . ' +  sentences[idx + 1]))
#                     else:
#                         rows.append((q['__id__'], p['id'] + '$$' + str(idx), q['question'], sen))
#             else:
#                 rows.append((q['__id__'], p['id'], q['question'], p['text']))    
#     with open('./data/dev_join2.tsv', 'w') as f:
#         writer = csv.writer(f, delimiter = '\t')
#         writer.writerow(('id', 'q_id', 'ans_id', 'question', 'answer', 'is_correct'))
#         for idx, row in enumerate(rows):
#             q_id, ans_id, question, ans = row 
#             writer.writerow((str(idx), q_id, ans_id, question, ans.replace('\t', ' '), 0))


def gather_oof_for_train():
    probs = None     
    probs_results = []
    with open('oof_train.txt', 'r') as f:
        probs = f.readlines()
        probs = [p.strip('\n') for p in probs]

    with open('./data/train.3.tsv', 'r') as f:
        reader = csv.reader(f, delimiter = '\t', quotechar=None)
        for idx, r in enumerate(reader):
            if idx == 0:
                continue
            _, q_id, _, _, _, _ = r            
            pos, neg = probs[idx-1].split(',')
            if len(probs_results) > 0:                        
                prev = probs_results[-1]                        
                prev_qid, prev_pos, prev_neg = prev 
                if prev_qid == q_id:
                    # already added 
                    if float(pos) > float(prev_pos):
                        probs_results[-1] = (q_id, pos, neg)
                    else:
                        # do nothing 
                        continue
                else:                        
                    probs_results.append((q_id, pos, neg))
            else:
                probs_results.append((q_id, pos, neg))

                # if probs is not None:
    with open('train_oof.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(('q_id', 'pos', 'neg'))
        for r in probs_results:
            writer.writerow(r)


def gather_oof(split_token='$$'):
    probs = None     
    probs_results = []
    with open('oof.txt', 'r') as f:
        probs = f.readlines()
        probs = [p.strip('\n') for p in probs]

    with open('./data/dev.tsv', 'r') as f:
        reader = csv.reader(f, delimiter = '\t')
        for idx, r in enumerate(reader):
            if idx == 0:
                continue
            _, q_id, ans_id, question, answer, _ = r
            pos, neg = probs[idx-1].split(',')
            if ans_id.find(split_token) >= 0:
                # print('????---> ', question)
                # print(answer)
                para_id = ans_id.split(split_token)[0]
                if len(probs_results) > 0:                        
                    prev = probs_results[-1]                        
                    prev_qid, prev_pid, prev_pos, prev_neg = prev 
                    if prev_qid == q_id and prev_pid == para_id:
                        # already added 
                        if float(pos) > float(prev_pos):
                            probs_results[-1] = (q_id, para_id, pos, neg)
                        else:
                            # do nothing 
                            continue
                    else:                        
                        probs_results.append((q_id, para_id, pos, neg))

            else:
                probs_results.append((q_id, ans_id, pos, neg))
                # if probs is not None:
    with open('test_oof.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(('q_id', 'para_id', 'pos', 'neg'))
        for r in probs_results:
            writer.writerow(r)

def gather_answer(split_token='$$'):
    is_corrects = None
    with open('pred_results.txt', 'r') as f:
        is_corrects = f.readlines()
    is_corrects = [int(x) for x in is_corrects]
    
    results = []
    with open('./data/dev.tsv', 'r') as f:
        reader = csv.reader(f, delimiter = '\t', quotechar=None)
        for idx, r in enumerate(reader):
            if idx == 0:
                continue
            _, q_id, ans_id, question, answer, _ = r
            is_correct = is_corrects[idx-1]
            if is_correct == 1:
                if ans_id.find(split_token) >= 0:
                    # print('????---> ', question)
                    # print(answer)
                    para_id = ans_id.split(split_token)[0]
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

def test_train_fm():
    # from transformers import glue_processors as processors
    # p = processors['qqp']()
    # p.get_labels()
    # p.get_train_examples('./data')
    with open('./data/train.tsv', 'r',  encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter='\t',  quotechar=None)
        for idx, line in enumerate(reader):
            if idx > 16986 and idx < 16990:
                print(idx, line)

def test_ner():
    content = None
    with open('./raw/train.json', 'r') as f:
        content = f.read()
    data = json.loads(content)
    names = set()
    for q in data:
        title = q['title']
        if q['label'] == True:
            entities = underthesea.ner(title)
            for idx, e in enumerate(entities):
                if e[-1] == 'B-PER':
                    txt = e[0]
                    # if txt == 'Na': print(entities)
                    if idx < len(entities) - 1 and entities[idx+1][-1] == 'I-PER':
                        txt += ' ' + entities[idx+1][0]
                    # print (txt)
                    if len(txt.split()) >= 2:
                        names.add(txt)
    print(names)
    print('total', len(names))
    with open('./data/names.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for n in list(names):
            writer.writerow((n,))
        # print([e for e in entities if e[-1] == 'B-PER'])

def get_mask_names():
    m = dict()
    with open('./data/names.csv', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for r in reader:
            # print(r)
            name, a = r
            # if a.strip() is not None: 
            if a is not None and not a.strip() == '':
                m[name] = a.strip()

    return m

def mask_name_in_text(text, ori, repl):
    return text.replace(ori, repl)

def mask_names_in_data():
    content = None
    with open('./raw/train.json', 'r') as f:
        content = f.read()
    data = json.loads(content)
    extra = []
    name_map = get_mask_names()
    for q in data:
        entities = underthesea.ner(q['title'])
        for idx, e in enumerate(entities):
            if e[-1] == 'B-PER':
                txt = e[0]
                # if txt == 'Na': print(entities)
                if idx < len(entities) - 1 and entities[idx+1][-1] == 'I-PER':
                    txt += ' ' + entities[idx+1][0]
                # print (txt)
                if txt in name_map:
                    # do masking here 
                    # make sure that actual name becomes not important 
                    new_text = mask_name_in_text(q['text'], txt, name_map[txt])
                    d = dict(label=q['label'], id=q['id'] + '_msk', question=q['question'], text=new_text, title=q['title'])
                    extra.append(d)
    print(len(extra))
    with open('./raw/masked_train.json', 'w') as f:
        json.dump(extra, f, indent=4, ensure_ascii=False)
    return extra

def split_data():
    lines = None
    with open('./data/all_train.tsv', 'r') as f:
        lines = f.readlines()
    header = lines[0]
    rest = lines[1:]
    shuffle(rest)
    train = [header] + rest[0:24100]
    val = [header] + rest[24100:]
    with open('./data/all_trainset.tsv', 'w') as f:
        f.writelines(train)
    with open('./data/all_valset.tsv', 'w') as f:
        f.writelines(val)


def check():
    
    with open('./data/bert_train.tsv', 'r') as f:
        reader = csv.reader(f, delimiter='\t', quotechar=None)
        with open('./data/bert_train_fixed.tsv', 'w') as o:
            writer = csv.writer(o, delimiter='\t', quotechar=None)

            for idx, r in enumerate(reader):
                if idx == 0:
                    writer.writerow(r)
                    continue
                r[0] = idx 
                writer.writerow(r)


if __name__ == '__main__':
    # new_main(model_type='xlnet')
    gather_answer()
    # test
    # gather_oof_for_train
    # a = []
    # b = []
    # q = False
    # with open('./data/train.3.tsv', 'r') as f:
    #     reader = csv.reader(f, delimiter = '\t', quotechar=None)
    #     for idx, r in enumerate(reader):
    #         if q:
    #             print(r)
    #             exit(0)
    #         a.append(r)
    #         if r[0] == '6567':
    #             print(r)
    #             q = True

    # with open('./data/train.3.tsv', 'r') as f:
    #     reader = csv.reader(f, delimiter = '\t')
    #     for r in reader:
    #         b.append(r)
    #         # if r[3].find('\t') >= 0 or r[4].find('\t') >= 0:
    #         for t in r: 
    #             if t.find('\t') >= 0 or t.find('\n') >= 0:
    #                 print (r)
    #                 exit(0) 

    # for i in range(0, len(b)):
    #     if not b[i] == a[i]:
    #         print(b[i])
    #         print(a[i])
    #         break