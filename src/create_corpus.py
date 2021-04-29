import sys

# data = sys.stdin.readlines()
# if data[0] == '\n':
#     data.pop()
check = 0
# for line in sys.stdin:
#     # line = data[index]
#     # if(line=='\n'):
#     if line.startswith('__'):
#         continue
#     elif line != '\n':
#         print(line.strip('\n'), end=' ')
#     elif line == '\n' and check == 0:
#         check = 1
#     else:
#         print()
#         check = 0

dict_pos = {
    "PROPN": "properNoun",
    "PUNCT": "punctuation",
    "ADJ": "adjective",
    "NOUN": "noun",
    "VERB": "verb",
    "DET": "determiner",
    "ADP": "adposition",
    "AUX": "auxiliary",
    "PRON": "pronoun",
    "PART": "particle",
    "SCONJ": "subordinatingConjunction",
    "NUM": "number",
    "ADV": "adverb",
    "CCONJ": "coordinatingConjunction",
    "INTJ": "interjection",
    "SYM": "symbol"
}
list_dict_key = list(dict_pos.keys())


def pos_lemonpos(x):
    if x not in list_dict_key:
        return 'none'
    else:
        return dict_pos[x]


for line in sys.stdin:
    # line = data[index]
    # if(line=='\n'):
    if line.startswith('\n'):
        print()
        continue
    elif line.startswith('# text'):
        continue
    else:
        try:
            elements = line.strip('\n').split('\t')
            if elements[2] == elements[3] == '_':
                continue
            else:
                print(elements[2].lower() + '_' + pos_lemonpos(elements[3]), end=' ')
        except:
            continue
