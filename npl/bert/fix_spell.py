import torch
from transformers import BertTokenizer, BertForMaskedLM
# from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM

# OPTIONAL: if you want to have more information on what's happening, activate the logger as follows
import logging
logging.basicConfig(level=logging.INFO)

# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', cache_dir=None, do_lower_case=False)

text = '[CLS] I want to [MASK] the car because it is cheap . [SEP]'
tokenized_text = tokenizer.tokenize(text)
indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

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

# print('predictions = ', predictions)
predicted_index = torch.argmax(predictions[0][0][masked_index]).item()
predicted_token = tokenizer.convert_ids_to_tokens([predicted_index])[0]

print(predicted_token)