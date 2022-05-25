import spacy
import re
import os
import pandas as pd

nlp = spacy.load('en_core_web_lg')

in_re = re.compile(r"[Ii]n (the )?\d{4} (year(s)?)|[Ii]n (the )?(year(s)?) (of )?\d{4}")
from_re = re.compile(r"[Ff]rom \d{2,4}(-\d{2})? (year(s)?)|[Ff]rom \d{2,4} to \d{2,4} (year(s)?)")
between_re = re.compile(r"[Bb]etween \d{2,4} (year(s)?)|[Bb]etween \d{2,4} and \d{2,4} (year(s)?)")
until_re = re.compile(r"[Uu]ntil \d{2,4} (year(s)?)")
be_re = re.compile(r"(be|am|is|are|was|were|aged|by) (over )?\d{2}(-\d{2})? (year(s)?)")
than_re = re.compile(r"(older|younger) (than )?\d{2} (year(s)?)")

old_re = re.compile(r"year(s)? old")
two_re = re.compile(r"[Ii]n the year 2\d{3}")

re_list = [be_re, between_re, from_re, in_re, than_re, until_re]

text_name_list = []
text_list = []
probable_error_span_list = []

for doc in os.listdir():
    if ".txt" in doc:
        with open(doc, "r", encoding="utf-8") as f:
            text = nlp(f.read())
            sents = list(text.sents)
            for sent in sents:
                for re in re_list:
                    if re.findall(sent.text) and not old_re.findall(sent.text) and not two_re.findall(sent.text):
                        for tuple in re.findall(sent.text):
                            for word in [i for i in tuple]:
                                if word == "year" or word == "years":
                                    probable_error_span_list.append(word)
                                    text_name_list.append(doc)
                                    text_list.append(sent)

data = {
    "text_name": text_name_list,
    "text": text_list,
    "probable_error_span": probable_error_span_list
}
df = pd.DataFrame(data) # датафрейм для записи ошибок
df = df.drop_duplicates(keep='first')
df.to_csv("years.csv", index=None)
