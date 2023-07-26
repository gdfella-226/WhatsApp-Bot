from tools.convert import convert
from os import listdir, path
from json import dump, load
from loguru import logger
import sqlite3


IMG_PATH = path.join('./', 'data')
CONFIG_PATH = path.join('./', 'config.json')
DB_PATH = path.join('./', 'database.db')


def db_handler() -> None:
    sqlite3.connect(DB_PATH)


def upd_params(new_params: dict) -> None:
    logger.info('Updating parameters...')
    with open(CONFIG_PATH, 'r') as fp:
        params = load(fp)
        params.update(new_params)
    with open(CONFIG_PATH, 'w') as fp:
        dump(params, fp)


def main() -> None:
    new_line = dict()
    for filename in listdir(IMG_PATH):
        logger.debug(f'Found img: {filename}')
        if 'passport' in filename:
            upd_params({"type": "passport", "path": path.abspath(path.join(IMG_PATH, filename)),
                        "preprocess": "", "language": "rus"})
        elif 'credit' in filename:
            upd_params({"type": "credit", "path": path.abspath(path.join(IMG_PATH, filename)),
                        "preprocess": "", "language": "rus"})
        elif 'insurance' in filename:
            upd_params({"type": "insurance", "path": path.abspath(path.join(IMG_PATH, filename)),
                        "preprocess": "Thresh", "language": "eng+rus"})
        elif 'additional' in filename:
            upd_params({"type": "additional", "path": path.abspath(path.join(IMG_PATH, filename)),
                        "preprocess": "", "language": "rus"})
        else:
            continue
        new_line.update(convert())
    logger.success(new_line)


if __name__ == '__main__':
    main()
