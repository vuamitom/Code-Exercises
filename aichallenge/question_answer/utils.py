from underthesea import sent_tokenize

stopwords = open('resources/stopwords_small.txt').read().split('\n')
stopwords = set([w.replace(' ','_') for w in stopwords])
punct_set = set(["... ",".. "])
max_punct_len = max([len(x) for x in punct_set])
min_punct_len = min([len(x) for x in punct_set])

def _check_missing_punct(text):
    toks = []
    i = 0
    last = 0
    while i < len(text):
        for c in reversed(range(min_punct_len, max_punct_len + 1)):
            if text[i:(i + c)] in punct_set:
                if i > last:
                    toks.append(('T', text[last:i]))
                toks.append(('P', text[i:(i+c)]))
                last = i + c
                i+=c-1
                break
        i +=1 
    if len(toks) > 0:
        if last < i:
            toks.append(('T', text[last:i]))

        res = []
        last = 0
        for idx, tok in enumerate(toks):
            if idx > 0 and idx < len(toks) -1:
                kind, val = tok
                if kind == 'P':                    
                    next_tok_kind, next_tok = toks[idx + 1]
                    if not next_tok_kind == 'T':
                        print ('WARNING ', toks)
                        continue                    
                    # check if it is captialized 
                    if next_tok[0].isupper():
                        # if yes, it should be another sentence 
                        res.append(''.join([val for _, val in toks[last:idx]]))
                        last = idx + 1
                    else:
                        continue
        if len(res) > 0:
            res.append(''.join([val for _, val in toks[last:]]))
            return res
        else:
            return [text]
    else:
        return [text]

def tokenize_sentence(text):
    sens = sent_tokenize(text)
    final = []
    for sen in sens:
        retok = _check_missing_punct(sen)
        final += retok

    # if crude is not None and len(final) < 2:
    #     for p in crude:
    #         final = []
    #         for sen in sens:
    #             final += sen.split('.')
    #         final = [s for s in final if len(s) > 0]
    return final

if __name__ == '__main__':
    sentences = tokenize_sentence('Một trận thi đấu bóng đá thông thường diễn ra trong hai hiệp chính thức liên tiếp , mỗi hiệp gồm 45 phút ngăn cách bằng 15 phút nghỉ giữa giờ . Sau khi hiệp 1 , hai đội bóng sẽ phải đổi sân cho nhau để có sự công bằng trong vòng 1 phút .')
    print(sentences)
    # rel_ranking('', sentences)
    sentences = tokenize_sentence('Cũng trong thập niên 1850 , các đội bóng nghiệp dư bắt đầu được thành lập và thường mỗi đội xây dựng cho riêng họ những luật chơi mới của môn bóng đá , trong đó đáng chú ý có câu lạc bộ Sheffield F.C .. Việc mỗi đội bóng có luật chơi khác nhau khiến việc điều hành mỗi trận đấu giữa họ diễn ra rất khó khăn .')
    print(sentences)

    sentences = tokenize_sentence("Lực lượng Dã chiến I , Việt Nam , còn gọi là Quân đoàn I Dã chiến , Việt Nam ( tiếng Anh : \" I Field Force , Vietnam \" - I.FFV ) là lực lượng cấp quân đoàn của lực lượng Quân đội Hoa Kỳ và đồng minh tại Việt Nam trong thời gian chiến tranh Việt Nam .")
    print(sentences)

    sentences = tokenize_sentence("Năm 2000 , ca sĩ Thu Phương với ca khúc \" Cô gái đến từ hôm qua \" của Trần Lê Quỳnh cũng đã gặt hái những thành công với giải thưởng \" Làn sóng xanh \" .")
    print(sentences)

    sentences = tokenize_sentence("Trong sách Đại Việt Sử ký Toàn thư , sử gia Ngô Sĩ Liên nhận định : \" \" Công đánh giặc Nguyên , Nhật Duật lập được nhiều hơn cả \" \" .")
    print(sentences)

    sentences = tokenize_sentence("ISO 4217 là một tiêu chuẩn của Tổ chức tiêu chuẩn hóa quốc tế (ISO) quy định về mã của tất cả các đơn vị tiền tệ bao gồm cả tiền tệ dùng trong giao dịch thanh toán và tiền tệ kế toán. ISO 4217 cũng mã hóa cho các đơn vị tiền tệ được định nghĩa là 1 troy ounce của các kim loại quý như vàng, bạc, platinum (vàng trắng)... Hệ thống mã này gồm hai loại mã, mã 3 ký tự bằng chữ (ví dụ: USD) và mã 3 ký tự bằng số (ví dụ: 704 cho đồng Việt Nam). Trừ một vài ngoại lệ, đối với tiền tệ của một quốc gia, mã 3 ký tự bằng chữ có hai ký tự đầu là mã quốc gia (cũng đã được chuẩn hóa theo một tiêu chuẩn khác của ISO) và ký tự thứ ba là chữ cái bắt đầu của tên gọi đơn vị tiền tệ, đồng Việt Nam được mã hóa theo đúng nguyên tắc này thành VND. Hệ thống mã này giúp cho các đơn vị tiền tệ được sử dụng trong thương mại, thanh toán một cách thống nhất và tránh được nhầm lẫn.")
    print(sentences)

    sentences = tokenize_sentence("và nhiều huyền thoại, truyền thuyết liên quan đến núi Hồng như: Ông Đùng xếp núi, truyền thuyết về kinh đô của Vua Hùng... và với 7 sắc phong và 1 công lệnh thời Lê,")
    print(sentences)

    sentences = tokenize_sentence("Ông tên thật là Trần Kim Cường, sinh ngày 21 tháng 12 năm 1936 tại Bến Tre, sau theo gia đình vào Sài Gòn. Ngay từ khi còn là học sinh Trường Trung học Trần Hưng Đạo, ông đã có thể tự sáng tác và biểu diễn những bài hát học sinh trong các lần hội diễn của trường. Sau khi học xong “tú tài”... , ông chính thức theo nghiệp ca hát tại các vũ trường Kim Sơn, Baccara,...")
    print(sentences)

    sentences = tokenize_sentence("Trong khoa đo lường, ppm là đơn vị đo mật độ thường dành cho các mật độ tương đối thấp. Nó thường chỉ tỷ lệ của lượng một chất trong tổng số lượng của hỗn hợp chứa chất đó. Ở đây lượng có thể hiểu là khối lượng, thể tích, số hạt (số mol),... ... Chữ ppm xuất phát từ tiếng Anh parts per million nghĩa là một phần triệu.")
    print(sentences)