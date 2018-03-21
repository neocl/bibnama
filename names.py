import csv
import nltk
import string
from collections import Counter
from collections import defaultdict as dd

PUNCS = list(string.punctuation) + ["``", "''"]
NO_PUNC = str.maketrans('', '', string.punctuation)


# read bible data
with open('bibid.csv', 'r', encoding= 'utf8') as infile:
    reader = csv.DictReader(infile)
    verses = [v for v in reader]

# tokenize
tc = Counter()
for v in verses:
    # remove tab
    if v['text'].startswith('<t />'):
        text = v['text'][5:]
    else:
        text = v['text']
    # tokenize
    tokens = nltk.word_tokenize(text)
    v['tokens'] = tokens
    tc.update(tk.translate(NO_PUNC) for tk in tokens if tk not in PUNCS)
lexicon = set(tc.keys())

# --------------------
# look for names
names = dd(set)
maybe_names = dd(set)
for vid, v in enumerate(verses):
    for tid, tk in enumerate(v['tokens']):
        token = tk.translate(NO_PUNC)  # remove punc
        if not token:
            continue
        elif token[0].isupper():
            # if it's the first token ...
            if token.upper() == token or tid == 0 or v['tokens'][tid - 1] == '``' or v['tokens'][tid - 1][-1] in '.!\'?':
                # check if the lowered is also in lexicon
                maybe_names[token].add(vid)
            else:
                names[token].add(vid)
print("Found names: {}".format(len(names)))
print("May be: {}".format(len(maybe_names)))
name_list = list(sorted(names))


# write to file
with open("name_freq.csv", "w") as outfile:
    writer = csv.writer(outfile, dialect='excel-tab', quoting=csv.QUOTE_MINIMAL)
    for word, freq in tc.most_common():
        if word in names:
            writer.writerow((word, freq))
print("Donezo")
