import spacy
import benepar
benepar.download('benepar_en3')
from benepar import BeneparComponent, NonConstituentException
import re
import os

nlp = spacy.load('en_core_web_lg')

ex_re = re.compile(r"(\(SBAR \(IN except\) \(S \(PP \(IN for\))|(\(IN except\) \(PP \(IN for\) \(SBAR \(IN that\))|(\(SBAR \(IN except\) \(SBAR \(IN for\))")

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe("benepar", config={"model": "benepar_en3"})

text_name_list = []
text_list = []
probable_error_span_list = []

for doc in os.listdir():
    if ".txt" in doc:
        with open(doc, "r", encoding="utf-8") as f:
            text = nlp(f.read())
            sents = list(text.sents)
            for sent in sents:
                if ex_re.findall(sent._.parse_string):
                    text_name_list.append(doc)
                    text_list.append(sent)
                    probable_error_span_list.append("for")

data = {
    "text_name": text_name_list,
    "text": text_list,
    "probable_error_span": probable_error_span_list
}
df = pd.DataFrame(data) # датафрейм для записи ошибок
df = df.drop_duplicates(keep='first')
df.to_csv("except_for.csv", index=None)