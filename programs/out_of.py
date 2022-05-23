import spacy
nlp = spacy.load('en_core_web_lg')
import os
import pandas as pd

with open("out_of2.txt", "r", encoding="utf-8") as f: # список фразовых глаголов с out of
    out_of_ph_v = f.readlines()
    for i in range(len(out_of_ph_v)):
        out_of_ph_v[i] = out_of_ph_v[i].strip()

text_name_list = []
text_list = []
probable_error_span_list = []

for doc in os.listdir():
    if ".txt" in doc:
        with open(doc, "r", encoding="utf-8") as f:
            text = nlp(f.read())
            sents = list(text.sents)
            for sent in sents:
                for token in sent:
                    if token.text == "out":
                        for i in [child for child in token.children]:
                            if i.text == "of":
                                if token.head.lemma_ in out_ph_v and token.head.lemma_ not in out_of_ph_v:
                                    text_name_list.append(doc)
                                    text_list.append(sent)
                                    probable_error_span_list.append("of")
                                if [child_2 for child_2 in i.children] == []:
                                    text_name_list.append(doc)
                                    text_list.append(sent)
                                    probable_error_span_list.append("of")

data = {
    "text_name": text_name_list,
    "text": text_list,
    "probable_error_span": probable_error_span_list
}
df = pd.DataFrame(data) # датафрейм для записи ошибок
df = df.drop_duplicates(keep='first')
df.to_csv("out_of.csv", index=None)