from loguru import logger
import sqlite3


class DBHanler:
    def __init__(self, path: str) -> None:
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS data
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                            full_name TEXT, 
                            birth_date TEXT,
                            passport_ser_num TEXT,
                            passport_extr_date TEXT,
                            passport_extr_code TEXT,
                            credit_contract_number TEXT,
                            credit_contract_term TEXT,
                            insurance_contract_num TEXT,
                            additional_services_contract_num TEXT);""")
        except Exception as err:
            logger.error(f'Database error: {err}')

    def push(self, data: dict) -> None:
        try:
            res = self.cur.execute('select * from data')
            names = list(map(lambda x: x[0], res.description))
            print(names)
            for i in names:
                if i not in list(data.keys()) and i != 'id':
                    data[i] = '?????'
        except Exception as err:
            logger.error(f'Comparing error: {err}')
        try:
            sql = f"""INSERT INTO data (full_name, birth_date, passport_ser_num, passport_extr_date, 
passport_extr_code, credit_contract_number, credit_contract_term, 
insurance_contract_num, additional_services_contract_num) VALUES 
('{data["full_name"]}', '{data["birth_date"]}', '{data["passport_ser_num"]}',
'{data["passport_extr_date"]}', '{data["passport_extr_code"]}', 
'{data["credit_contract_number"]}', '{data["credit_contract_term"]}', 
'{data["insurance_contract_num"]}', '{data["additional_services_contract_num"]}');"""
            self.cur.execute(sql)
            self.conn.commit()
            logger.debug('Successfully insert data to DB!')
        except Exception as err:
            logger.error(f'Database error: {err}')

    def clear(self):
        try:
            self.cur.execute('DROP TABLE IF EXISTS data;')
        except Exception as err:
            logger.error(f'Database error: {err}')


if __name__ == "__main__":
    TEST_DATA = {
          'additional_services_contract_num': '0051900379', 'credit_contract_number': '00319-С+-000000458509',
          'credit_contract_term': '60 месяцев', 'insurance_contract_num': 'OOBSEBI104100226055',
          'full_name': 'Дейнего Владислав Николаевич', 'birth_date': '12.03.1964', 'passport_ser_num': '6019-767612',
          'passport_extr_code': '610_069'
    }

    DB_PATH = "C:\\Users\\Danil\\Documents\\Projects\\WhatsApp-Bot\\database.db"
    dbh = DBHanler(DB_PATH)
    dbh.push(TEST_DATA)
    dbh.clear()
