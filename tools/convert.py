"""
    Contains methods to recognize documents and read text from ones
    Convert row of images to json(dict)
"""
from re import search
from os import path, getpid, listdir, unlink, mkdir
from json import load
from codecs import open
import cv2
import pytesseract
from shutil import rmtree
from PIL import Image
from loguru import logger
from tools.vocabulary import encode_name


CONFIG_PATH = path.abspath(path.join('./', 'config.json'))


def clear_directory(folder: str) -> None:
    """
        Remove all files from chosen directory
        :param folder: path to directory
    """
    for filename in listdir(folder):
        file_path = path.join(folder, filename)
        try:
            if path.isfile(file_path) or path.islink(file_path):
                unlink(file_path)
            elif path.isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            logger.error(f'Failed to clear dir: {e}')


def process_img(img: cv2.UMat, params: str) -> cv2.UMat:
    """
    Method to processing images for better text recognising
    Provides ability to:
        - Convert image to B&W;
        - Increase contrast;
        - Set Threshold;
        - Use blur.
    :param img: CV2's image-object
    :param params: String contains information about processing.
        (ex: param1+param2+..+paramN)
        IMPORTANT: Has more priority than params from 'config.json'
        Possible parameters:
            Ctrs (Contrast);
            Thresh (Threshold);
            Blur.
    :return: processed CV2's image-object
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if params:
        if 'Ctrs' in params:
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l_channel, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l_channel)
            limg = cv2.merge((cl, a, b))
            enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
            img = enhanced_img

        if 'Thresh' in params:
            img = cv2.threshold(img, 0, 255,
                                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        if 'Blur' in params:
            img = cv2.medianBlur(img, 3)

    return img


def convert_img(custom_params: dict = None) -> str:
    """
        Recognize text from image
        :param custom_params: Custom parameters (have higher priority than config-file)
        :return: Characters found in image
    """
    PARAMS = load(open(CONFIG_PATH, 'r'))
    if not path.isdir('./tmp'):
        mkdir('./tmp')

    if custom_params:
        for key, value in custom_params.items():
            PARAMS[key] = value

    image = cv2.imread(PARAMS['path'])
    if PARAMS['preprocess']:
        image = process_img(image, PARAMS["preprocess"])
    filename = path.abspath(path.join('./tmp', f'processed{getpid()}.png'))
    cv2.imwrite(filename, image)
    text = pytesseract.image_to_string(Image.open(filename), lang=PARAMS['language'])
    f = open(path.join('./tmp', f'output{getpid()}.txt'), 'w', 'utf-16')
    f.write(text)
    f.close()
    return text


def parse_passport(chars: str) -> dict:
    """
        Get data from recognized text for passport
        :param chars: Unprocessed text-data
        :return: Text in usable format
    """
    logger.info('Scanning passport...')
    arr = [i.replace(' ', '') for i in chars.split('\n') if '<' in i]
    birth_date = arr[1][13:19]
    if int(birth_date[:2]) > 30:
        birth_date = '19' + birth_date
    else:
        birth_date = '20' + birth_date
    birth_date = birth_date[-2:] + '.' + birth_date[4:6] + '.' + birth_date[:4]

    res = dict()
    res['full_name'] = ' '.join([encode_name(i) for i in arr[0][5::].split('<') if i][0:3])
    res['birth_date'] = birth_date
    res['pass_ser_num'] = arr[1][0:3] + arr[1][30] + '-' + arr[1][3:9]
    try:
        res['pass_extr_code'] = search(r'\d\d\d-\d\d\d', chars).group()
        res['pass_extr_date'] = search(r'\d\d\.\d\d\.\d\d\d\d', chars).group()
        logger.debug(f'Success! {res}')
    except Exception as err:
        logger.error(f'Failed to parse extradition data: {err}')
        pass
    return res


def parse_credit(chars: str) -> dict:
    """
        Get data from recognized text for credit contract
        :param chars: Unprocessed text-data
        :return: Text in usable format
    """
    logger.info('Scanning credit contract...')
    chars = chars.lower().replace(' ', '')
    arr = [i for i in chars.split('\n\n') if i]
    res = dict()
    for line in arr:
        line.replace('\n', '')
        if search(r'договор\w*№', line):
            res["credit_number"] = line[line.find('№') + 1::].upper()
        elif "сумма:" in line:
            res["credit_sum"] = line[line.find(':') + 1: line.find('рублей')] + " рублей"
        elif "срокполноговозвратакредита" in line:
            res["credit_term"] = line[line.find('составляет') + 10: line.find('месяц')] + " месяцев"
    logger.debug(f'Success! {res}')
    return res


def parse_insurance(chars: str) -> dict:
    """
        Get data from recognized text for insurance contract
        :param chars: Unprocessed text-data
        :return: Text in usable format
    """
    logger.info('Scanning insurance contract...')
    arr = [i for i in chars.split('\n') if i]
    res = dict()
    try:
        for line in arr:
            if search(r':.\w*', line):
                res['ins_ser_num'] = search(r':.\w*', line).group()[2::]
                break
                # date = line[line.find('ОТ')+2::]
                # print(date)
        logger.debug(f'Success! {res}')
    except Exception as err:
        logger.error(f'Failed to parse data: {err}')
        res['ins_ser_num'] = '?????'
    return res


def parse_additional(chars: str) -> dict:
    """
        Get data from recognized text for additional services contract
        :param chars: Unprocessed text-data
        :return: Text in usable format
    """
    logger.info('Scanning additional services contract...')
    arr = [i for i in chars.split('\n') if i]
    res = dict()
    try:
        for line in arr:
            if "№" in line:
                found = search(r'№.*\d', line).group()
                ser_num = ''
                for i in found:
                    if i.isdigit():
                        ser_num += i
                res['add_ser_num'] = ser_num
                break
        logger.debug(f'Success! {res}')
    except Exception as err:
        logger.error(f'Failed to parse data: {err}')
        res['add_ser_num'] = '?????'
    return res


def convert():
    """
        Get type of document from 'config.json' and call suitable parse-function
    """
    PARAMS = load(open(CONFIG_PATH, 'r'))
    doc = PARAMS['type']
    data = None
    if doc == 'passport':
        data = parse_passport(convert_img({"language": "eng"}))
    elif doc == 'credit':
        data = parse_credit(convert_img({"language": "rus"}))
    elif doc == 'insurance':
        data = parse_insurance(convert_img())
    elif doc == 'additional':
        data = parse_additional(convert_img())
    # logger.debug(data)

    # input('pause...')
    clear_directory('../tmp')
    return data


if __name__ == '__main__':
    convert()
