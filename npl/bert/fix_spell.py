import torch
from transformers import BertTokenizer, BertForMaskedLM
# from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM

# OPTIONAL: if you want to have more information on what's happening, activate the logger as follows
import logging
logging.basicConfig(level=logging.INFO)

# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', cache_dir=None, do_lower_case=False)
print('tokenizer len = ' + str(len(tokenizer)))
text = '[CLS] Công cha như [MASK] thái sơn . [SEP]'
tokenized_text = tokenizer.tokenize(text)
print('tokenized text === ', tokenized_text)
indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
print('indexed_tokens === ', indexed_tokens)
# Create the segments tensors.
segments_ids = [0] * len(tokenized_text)

# Convert inputs to PyTorch tensors
tokens_tensor = torch.tensor([indexed_tokens])
segments_tensors = torch.tensor([segments_ids])

# Load pre-trained model (weights)
model = BertForMaskedLM.from_pretrained('bert-base-multilingual-cased', cache_dir=None)
model.eval()

masked_index = tokenized_text.index('[MASK]') 
print('masked_index == ', masked_index)

# Predict all tokens
with torch.no_grad():
    predictions = model(tokens_tensor, segments_tensors)

print('len of words token  = ', len(predictions[0][0]))
predicted_index = torch.argmax(predictions[0][0][masked_index]).item()
predicted_token = tokenizer.convert_ids_to_tokens([predicted_index])[0]

print('MASK ===== ', predicted_token)

print(tokenizer.tokenize('HLV Park Hang-xeo và đội ngũ của mình vẫn còn nhiều câu hỏi cần lời giải trong thời gian tới. Cristaino Ronaldo được hãng Nike thửa riêng đôi giày mang tên \'CR7 đẹp chai\' trước chuyến du dấu châu Á của Juventus.'))

tokenizer.add_tokens('HLV Park Hang-xeo và đội ngũ của mình vẫn còn nhiều câu hỏi cần lời giải trong thời gian tới'.split(' '))
tokenizer.add_tokens(['Cristaino Ronaldo'] + 'được hãng Nike thửa riêng đôi giày mang tên CR7 trước chuyến du dấu châu Á của Juventus'.split(' '))
# model.resize_token_embeddings(len(tokenizer))
print(tokenizer.tokenize('HLV Park Hang-xeo và đội ngũ của mình vẫn còn nhiều câu hỏi cần lời giải trong thời gian tới. Cristaino Ronaldo được hãng Nike thửa riêng đôi giày mang tên \'CR7 đẹp chai\' trước chuyến du dấu châu Á của Juventus.'))