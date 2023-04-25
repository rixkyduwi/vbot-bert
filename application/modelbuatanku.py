import torch
from transformers import BertForQuestionAnswering, BertTokenizer, BertTokenizerFast
from nlpcnn import nlp

#Model
#model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = BertForQuestionAnswering.from_pretrained("model",return_dict= False)

#Tokenizer
#tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained("indolem/indobert-base-uncased")
print(tokenizer)

question = '''random ?'''


filter = nlp(question)

print(filter)

paragraph = '''maag atau sindrom dispepsia adalah penyakit yang mempunyai gejala Nyeri ulu hati, mual, dan muntah setelah makan'''

isi_kata = paragraph.split()
print(isi_kata)
filter_kata = question.split()
print(filter_kata)
kata_benar = 0



for katakonteks in filter_kata:
    for kataquestion in isi_kata:
        if katakonteks == kataquestion:
            kata_benar = kata_benar+1
            print("benar")
        else:
            print("salah tapi..")
            huruf_benar = 0
            hrfkonteks = list(katakonteks)
            hrfquestion = list(kataquestion)
            print(hrfkonteks)
            print(len(hrfkonteks))
            print(hrfquestion)
            print(len(hrfquestion))
            if len(hrfkonteks) == len(hrfquestion):
                for hrfindeks in range(len(hrfkonteks)):
                    if(hrfindeks<=len(hrfquestion)-1):
                        print(hrfkonteks[hrfindeks])
                        print(hrfquestion[hrfindeks])
                        print(len(hrfquestion)-1)
                        if hrfkonteks[hrfindeks] == hrfquestion[hrfindeks]:
                            print("huruf benar +1")
                            huruf_benar = huruf_benar+1
            print(huruf_benar)
            print(len(hrfquestion)-1)
            if huruf_benar >= len(hrfquestion)-1:
                kata_benar = kata_benar+1
                print("ternyata typo dikit jadi.. benar")
            else:
                print("ternyata memang salah")
            

            
print(kata_benar)


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
