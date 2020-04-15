import string
from utils import stopwords
from synonyms import generateVariants

punct_set = set([c for c in string.punctuation]) | set(['“','”',"...","–","…","..","•",'“','”'])
punct_set_str = ''.join(list(punct_set))

def generateNgram(paper, ngram = 2, deli = '_', rmSet = {}):
    words = paper.split()
    if len(words) == 1:
        return ''
    words = [w.strip(punct_set_str) for w in words]
    
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
        # print (p_unigram)
        # print (q_ngrams['unigram'])
        p_trigram = set(generateNgram(sentence,3,'_',punct_set | stopwords))
        p_fourgram= set(generateNgram(sentence,4,'_',punct_set))
        # print ('----------------------------->')
        # print(p_unigram & q_ngrams['unigram'])
        # print(p_bigram & q_ngrams['bigram'])
        # print(p_trigram & q_ngrams['trigram'])
        # print(p_fourgram & q_ngrams['fourgram'])
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
    # print (q_variants)   
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

    # sentences = tokenize_sentence('Quân đội Hoa Kỳ hay Các lực lượng vũ trang Hoa Kỳ là tổng hợp các lực lượng quân sự thống nhất của Hoa Kỳ . Các lực lượng này gồm có Lục quân , Hải quân , Thuỷ quân lục chiến , Không quân và Tuần duyên .')
    # # print(sentences)
    # question = 'Quân đội Hoa Kỳ gồm những lực lượng nào'
    # print (rel_ranking(question, sentences))

    # question = 'Đạo Hồi xuất phát từ quốc gia nào'
    # sentences = tokenize_sentence("Đối với người ngoài, đạo Hồi ra đời vào thế kỷ 7 tại bán đảo Ả Rập, do Thiên sứ Muhammad nhận mặc khải của thượng đế truyền lại cho con người qua thiên thần Jibrael (Gabriel). Đạo Hồi chỉ tôn thờ Allah Đấng Tối cao, Đấng Duy Nhất (tiếng Ả Rập: الله \"Allāh\"). Đối với tín đồ, Muhammad là vị Thiên Sứ cuối cùng được Allah mặc khải Thiên Kinh Qur'an (còn viết là Koran) qua Thiên thần Jibrael.")
    # print (rel_ranking(question, sentences))

    # question = 'Quốc gia nào là quê hương của ông già Noel'
    # sentences = tokenize_sentence("So với những quốc gia Bắc Âu được cho là xuất xứ của ông già Noel, Phần Lan có vẻ được biết đến nhiều hơn hết. Là một đất nước nổi tiếng về du lịch mùa đông và tuyết, cùng những món ăn đặc sản như cá hồi và thịt tuần lộc, ông già Noel cũng là biểu tượng văn hóa du lịch của Phần Lan. Người ta cho rằng ông già Noel cư ngụ tại Lapland, miền Bắc Phần Lan. Thành phố Rovaniemi, thủ đô của vùng Lapland, được xem là thủ phủ của ông già Noel.")

    # print (rel_ranking(question, sentences))

    # question = "Bức tranh Mona Lisa hiện đang được trưng bày ở đâu"
    # sentences = tokenize_sentence("Bức hoạ Mona Lisa hiện được treo tại Bảo tàng Louvre ở Paris , Pháp . Danh tiếng ngày càng tăng của bức hoạ còn lớn thêm khi nó bị ăn trộm ngày 21 tháng 8 năm 1911 . Ngày hôm sau , Louis Béroud , một hoạ sĩ , đi vào Louvre và vào Salon Carré nơi bức tranh \" Mona Lisa \" đã được trưng bày trong năm năm .")
    # print (rel_ranking(question, sentences))

    # question = "Địa danh núi Bà Đen thuộc tỉnh nào"
    # sentences = tokenize_sentence("Thằn lằn núi Bà Đen hay thằn lằn ba sọc hoặc thằn lằn vạch (danh pháp hai phần: Cyrtodactylus badenensis), là một loài bò sát thuộc họ Tắc kè (\"Gekkonidae\"), Loài này được phát hiện ở núi Bà Đen, tỉnh Tây Ninh và được các tác giả Nguyễn Ngọc Sang, Nikolai L. Orlov và Ilya S. Darevsky mô tả năm 2006. Loại thằn lằn này là một món ăn đặc sản của Tây Ninh và được đồn đại là có thể chữa nhiều bệnh trong đó có bệnh ung thư.")
    # print (rel_ranking(question, sentences))

    # question = "Đơn vị tiền tệ của Thái Lan là gì"
    # sentences = tokenize_sentence("Cho đến ngày 27 tháng 11 năm 1902, đồng tical đã được cố định trên một cơ sở bạc ròng, với 15 g bạc là 1 bạt. Điều này khiến cho giá trị đơn vị tiền tệ của Thái Lan dễ biến động so với các đồng tiền theo chế độ bản vị vàng. Năm 1857, giá trị của một số đồng tiền bạc nhất định đã được cố định theo quy định của pháp luật, với 1 bạt= 0,6 Straits dollar và 5 bạt = 7 rupee Ấn Độ. Trước năm 1880, tỷ giá hối đoái đã được cố định ở mức 8 bạt một Bảng Anh, song đã tụt xuống 10 bạt một bảng trong thập niên 1880.")
    # print (rel_ranking(question, sentences))

    # question = "Ngọn núi nào ở Nhật Bản được công nhận Di sản văn hóa thế giới"
    # sentences = tokenize_sentence("Nó là một trong \"Ba núi Thánh\" của Nhật Bản (三霊山, Sanreizan) cùng với Núi Haku và Tate. Phú Sĩ là một danh thắng đặc biệt và một di tích lịch sử của Nhật Bản.[7] Ngọn núi được thêm vào danh sách Di sản thế giới của UNESCO vào ngày 22 tháng 6 năm 2013 nhờ giá trị văn hóa. Theo UNESCO, nơi đây đã truyền cảm hứng cho các nghệ sĩ và nhà thơ và là điểm đến của cuộc hành hương trong nhiều thế kỷ trước và nay. Di sản này bao gồm 25 địa điểm nằm trong khu vực núi Phú Sĩ bao gồm khu vực núi thiêng, đền thờ Thần đạo Fujisan Hongū Sengen Taisha, đền thờ Phật giáo Taiseki-ji.")
    # print (rel_ranking(question, sentences))

    # question = "Ngôn ngữ chính thức của người dân Iceland là"
    # sentences = tokenize_sentence("Người Iceland rất tự hào về đất nước mình. Họ tự hào về di sản văn hóa Viking được thừa hưởng và ngôn ngữ riêng của họ, tiếng Iceland. Người dân Iceland rất quan tâm đến việc bảo vệ truyền thống văn hóa và ngôn ngữ của mình. Những lễ hội phổ biến ở Iceland là Ngày Quốc khánh vào ngày 17 tháng 6 để kỉ niệm ngày Iceland giành độc lập dân tộc năm 1944, lễ hội \"Sumardagurinn fyrsti\" được tổ chức ngày đầu tiên của mùa hè và lễ hội \"Sjómannadagurinn\" được tổ chức vào mỗi tháng 6 để nhớ ơn những chuyến vượt biển của tổ tiên đến Iceland.")
    # # sentences = tokenize_sentence('Họ tự hào về di sản văn hóa Viking được thừa hưởng và ngôn ngữ riêng của họ, tiếng Iceland')
    # print (rel_ranking(question, sentences))

    question = "Con vật đầu tiên được nhân bản vô tính thành công"
    sentences = tokenize_sentence("Một con cừu mouflon đã nhân bản thành công vào đầu năm 2001 và đã sống ít nhất bảy tháng, khiến nó trở thành bản sao đầu tiên của một động vật có vú bị đe dọa để tồn tại. Sau hàng loạt thất bại trong việc nhân bản vô tính thú hoang, các nhà khoa học châu Âu đã công bố thành tựu về một con cừu mouflon quý hiếm được nhân bản đã trải qua 6 tháng tuổi mà không gặp sự cố nào.Con cừu cái này đang được chăm sóc tại Trung tâm Cứu hộ động vật hoang dã ở Sardinia, Italia. Để tạo ra con cừu mouflon này, nhóm khoa học của Đại học Teramo đã áp dụng kỹ thuật tương tự như kỹ thuật đã thành công trên cừu Dolly. ADN được trích ra từ xác của một con cừu cái đã chết trong Trung tâm Cứu hộ động vật hoang dã ở Sardinia.")
    # sentences = tokenize_sentence("Ak̠sum) là một thành phố ở bắc Ethiopia.")
    print (rel_ranking(question, sentences))