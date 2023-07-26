"""
    Contains dictionaries and tools to transform text-data
"""
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

months = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12'
}


def encode_name(word: str) -> str:
    """
        Transform full name from bottom of passport to default type
        :param word: full name coded by latin symbols and digits
        :return: full name in cyrillic symbols
    """
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


def encode_month(date: str) -> str:
    """
        Transform month in date to number: 'Январь' -> '01'
        :param date: full date (12 Января 2023)
        :return: date in digits: 12.01.2023
    """
    date = date.replace(' ', '')
    month = ""
    start = 0
    tmp = 0
    for i in date:
        if i.isalpha():
            month += i
            start = tmp
        else:
            tmp += 1

    for key, value in months.items():
        if month in key:
            return date[:start] + '.' + value + '.' + date[start+len(month):]
    return date
