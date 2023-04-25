import torch
from transformers import BertForQuestionAnswering, BertTokenizer, BertTokenizerFast
from nlpcnn import nlp

#Model
#model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = BertForQuestionAnswering.from_pretrained("indolem/indobert-base-uncased",return_dict= False)

#Tokenizer
#tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained("indolem/indobert-base-uncased")
print(tokenizer)

question = '''random ?'''


paragraph = '''maag atau sindrom dispepsia adalah penyakit yang mempunyai gejala Nyeri ulu hati , mual , dan muntah setelah makan'''


encoding = tokenizer.encode_plus(text=question,text_pair=paragraph)
print(encoding)

inputs = encoding['input_ids']  #Token embeddings
print(inputs)

sentence_embedding = encoding['token_type_ids']  #Segment embeddings
print(sentence_embedding)

tokens = tokenizer.convert_ids_to_tokens(inputs) #input tokens
print(tokens)
start_scores, end_scores = model(input_ids=torch.tensor([inputs]), token_type_ids=torch.tensor([sentence_embedding]))
print(start_scores, end_scores)
print(start_scores)
start_index = torch.argmax(start_scores)
print(start_index)
end_index = torch.argmax(end_scores)
print(end_index)
answer = ' '.join(tokens[start_index:end_index+1])
print(answer)
corrected_answer = ''
for word in answer.split():
    #If it's a subword token
    if word[0:2] == '##':
        corrected_answer += word[2:]
    else:
        corrected_answer += ' ' + word
print(corrected_answer)
if corrected_answer == "":
    print("maaf saya tidak tahu")
else:
    print("jawabannya adalah : "+corrected_answer)
