import os

import cv2
import pytesseract
import re
from os import path, getpid, remove
from PIL import Image
from json import load
from codecs import open
from vocabulary import encode

config_path = path.join('../', 'config.json')
PARAMS = load(open(config_path, 'r'))


def covert_img() -> str:
    """
    Recognize text from image
    :return: Characters found in image
    """
    if not path.isdir('../tmp'):
        os.mkdir('../tmp')
    image = cv2.imread(PARAMS['pathToImg'])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if 'Thresh' in PARAMS['preprocess']:
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    if 'Blur' in PARAMS['preprocess']:
        gray = cv2.medianBlur(gray, 3)

    filename = path.join('../tmp', f'processed{getpid()}.png')
    cv2.imwrite(filename, gray)
    # cv2.imshow('Output' gray)
    text = pytesseract.image_to_string(Image.open(filename), lang=PARAMS['language']).replace(' ', '')
    # remove(filename)
    f = open(path.join('../tmp', f'output{getpid()}.txt'), 'w', 'utf-16')
    f.write(text)
    f.close()
    # print(text)
    # input('Pause…')
    return text


def parse_text(chars: str) -> dict:
    """
    Get data from recognized text
    :param chars: Unprocessed text-data
    :return: Text in usable format
    """
    arr = [i for i in chars.split('\n') if '<' in i]

    res = dict()
    res['extr_date'] = re.search(r'\d\d\.\d\d\.\d\d\d\d', chars).group()
    res['extr_code'] = re.search(r'\d\d\d-\d\d\d', chars).group()
    tmp = re.search(r'\d+RUS\d+', chars).group()
    bd_idx = tmp.find('RUS') + 3
    birth_date = tmp[bd_idx + 4: bd_idx + 6] + '.' + \
                 tmp[bd_idx + 2: bd_idx + 4] + '.'
    if int(tmp[bd_idx: bd_idx + 3]) > 30:
        birth_date += '19' + tmp[bd_idx: bd_idx + 2]
    else:
        birth_date += '20' + tmp[bd_idx: bd_idx + 2]
    res['birth_date'] = birth_date
    res['full_name'] = ' '.join([encode(i) for i in arr[0][5::].split('<') if i][0:3])
    return res


if __name__ == '__main__':
    print(parse_text(covert_img()))
