import string
from utils import stopwords

punct_set = set([c for c in string.punctuation]) | set(['“','”',"...","–","…","..","•",'“','”'])

def generateNgram(paper, ngram = 2, deli = '_', rmSet = {}):
    words = paper.split()
    if len(words) == 1:
        return ''
    
    ngrams = []
    for i in range(0,len(words) - ngram + 1):
        block = words[i:i + ngram]
        if not any(w in rmSet for w in block):
            ngrams.append(deli.join(block))
            
    return ngrams

def sentence_score(q_ngrams, sentence):
    try:
        sentence = sentence.lower()

        p_unigram = set(generateNgram(sentence,1,'_',punct_set | stopwords))
        
        uni_score = len(p_unigram & q_ngrams['unigram'])

        p_bigram  = set(generateNgram(sentence,2,'_',punct_set | stopwords))
        p_trigram = set(generateNgram(sentence,3,'_',punct_set | stopwords))
        p_fourgram= set(generateNgram(sentence,4,'_',punct_set))

        bi_score = len(p_bigram & q_ngrams['bigram'])
        tri_score = len(p_trigram & q_ngrams['trigram'])
        four_score = len(p_fourgram & q_ngrams['fourgram'])

        #emd_sim = embedding_similarity(' '.join(p_unigram),' '.join(q_ngrams['unigram']))
        emd_sim = 0

        return uni_score + bi_score*2 + tri_score*3 + four_score*4 + emd_sim*3
    except:
        return 0


def rel_ranking(question, sentences):    
    #Return ranked list of passages from list of documents    
    q_variants = generateVariants(question)
    q_ngrams = {'unigram': set(generateNgram(question.lower(),1,'_',punct_set | stopwords))
                , 'bigram' : set([]), 'trigram': set([]), 'fourgram': set([])}

    for q in q_variants:
        q = q.lower()
        q_ngrams['bigram']  = q_ngrams['bigram']   | set(generateNgram(q,2,'_',punct_set | stopwords))
        q_ngrams['trigram'] = q_ngrams['trigram']  | set(generateNgram(q,3,'_',punct_set | stopwords))
        q_ngrams['fourgram']= q_ngrams['fourgram'] | set(generateNgram(q,4,'_',punct_set))

    p_scores = [(sentence_score(q_ngrams, p), p) for p in sentences]
    p_scores.sort(key=lambda x: -x[0])

    return p_scores

if __name__ == '__main__':
    from utils import tokenize_sentence
    sentences = tokenize_sentence('Một trận thi đấu bóng đá thông thường diễn ra trong hai hiệp chính thức liên tiếp , mỗi hiệp gồm 45 phút ngăn cách bằng 15 phút nghỉ giữa giờ . Sau khi hiệp 1 , hai đội bóng sẽ phải đổi sân cho nhau để có sự công bằng trong vòng 1 phút .')
    print(sentences)
    # rel_ranking('', sentences)
    sentences = tokenize_sentence('Cũng trong thập niên 1850 , các đội bóng nghiệp dư bắt đầu được thành lập và thường mỗi đội xây dựng cho riêng họ những luật chơi mới của môn bóng đá , trong đó đáng chú ý có câu lạc bộ Sheffield F.C . Việc mỗi đội bóng có luật chơi khác nhau khiến việc điều hành mỗi trận đấu giữa họ diễn ra rất khó khăn .')
    print(sentences)
