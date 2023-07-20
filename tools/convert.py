import os
import cv2
import pytesseract
from re import search
from os import path, getpid, listdir, unlink
from shutil import rmtree
from PIL import Image
from json import load
from codecs import open
from vocabulary import encode

config_path = path.join('../', 'config.json')
PARAMS = load(open(config_path, 'r'))


def clear_directory(folder):
    for filename in listdir(folder):
        file_path = path.join(folder, filename)
        try:
            if path.isfile(file_path) or path.islink(file_path):
                unlink(file_path)
            elif path.isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            print(f'Failed to clear dir: {e}')


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
    text = pytesseract.image_to_string(Image.open(filename), lang=PARAMS['language'])
    f = open(path.join('../tmp', f'output{getpid()}.txt'), 'w', 'utf-16')
    f.write(text)
    f.close()
    return text


def parse_text(chars: str) -> dict:
    """
    Get data from recognized text
    :param chars: Unprocessed text-data
    :return: Text in usable format
    """
    arr = [i.replace(' ', '') for i in chars.split('\n') if '<' in i]
    birth_date = arr[1][13:19]
    if int(birth_date[:2]) > 30:
        birth_date = '19' + birth_date
    else:
        birth_date = '20' + birth_date
    birth_date = birth_date[-2:] + '.' + birth_date[4:6] + '.' + birth_date[:4]

    res = dict()
    res['full_name'] = ' '.join([encode(i) for i in arr[0][5::].split('<') if i][0:3])
    res['birth_date'] = birth_date
    res['ser_num'] = arr[1][0:3] + arr[1][30] + '-' + arr[1][3:9]
    try:
        res['extr_code'] = search(r'\d\d\d-\d\d\d', chars).group()
        res['extr_date'] = search(r'\d\d\.\d\d\.\d\d\d\d', chars).group()
    except Exception as err:
        print(f'Failed to parse extradition data: {err}')
        pass
    return res


if __name__ == '__main__':
    print(parse_text(covert_img()))
    input('pause...')
    # clear_directory('../tmp')
