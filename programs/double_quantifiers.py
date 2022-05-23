import spacy
nlp = spacy.load('en_core_web_lg')
import os
import pandas as pd

ok_det = ["the", "a", "an", "this", "that", "such", "quite", "these", "those", "which", "both", "all"]
quantif = ["number", "numbers", "amount", "amounts", "hundreds", "thousands", "millions", "billions", "lot", "lots", "plenty", "deal"]

text_name_list = []
text_list = []
probable_error_span_list = []

for doc in os.listdir():
    if ".txt" in doc:
        with open(doc, "r", encoding = "utf-8") as f:
            text = nlp(f.read())
            for sent in text.sents:
                for token in sent:
                    if token.text in ["amount", "amounts", "number", "numbers"]:
                        for child in [i for i in token.children]:
                            if child.pos_ == "DET" and child.text.lower() not in ok_det and "of" in [str(i) for i in token.children]:
                                text_name_list.append(doc)
                                text_list.append(sent)
                                probable_error_span_list.append(child.text + " " + token.text)
                    if token.text in quantif:
                        for child in [i for i in token.children]:
                            if child.text.lower() == "of":
                                for child_2 in [j for j in child.children]:
                                    if child_2.text in quantif and "of" in [str(k) for k in child_2.children]:
                                        text_name_list.append(doc)
                                        text_list.append(sent)
                                        probable_error_span_list.append(token.text + " " + child.text + " " + child_2.text + " " + "of")


data = {
    "text_name": text_name_list,
    "text": text_list,
    "probable_error_span": probable_error_span_list
}
df = pd.DataFrame(data) # датафрейм для записи ошибок
df = df.drop_duplicates(keep='first')
df.to_csv("double_quantifiers.csv", index=None)