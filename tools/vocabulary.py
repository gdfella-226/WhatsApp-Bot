vocabulary = {
    'а': "A",
    'б': "B",
    'в': "V",
    'г': "G",
    'д': "D",
    'е': "E",
    'ё': "-",
    'ж': "-",
    'з': "Z",
    'и': "I",
    'й': "Q",
    'к': "K",
    'л': "L",
    'м': "M",
    'н': "N",
    'о': "O",
    'п': "P",
    'р': "R",
    'с': "S",
    'т': "T",
    'у': "U",
    'ф': "F",
    'х': "-",
    'ц': "-",
    'ч': "3",
    'ш': "4",
    'щ': "",
    'ъ': "",
    'ы': "",
    'ь': "9",
    'э': "6",
    'ю': "7",
    'я': "8"
}


def encode(word: str):
    word = word.upper()
    vals = list(vocabulary.values())
    res = ""
    for i in range(len(word)):
        if word[i] in vals:
            res += list(vocabulary.keys())[vals.index(word[i])]
        else:
            res += "?"
    res = res[0].upper() + res[1::]
    return res