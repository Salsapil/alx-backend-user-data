#!/usr/bin/env python3
"""Regex-ing"""
import re
from typing import List
import logging
import mysql.connector
import os


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format method """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ filter datum """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_logger() -> logging.Logger:
    """ Returns a logging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    target_handler = logging.StreamHandler()
    target_handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))
    target_handler.setFormatter(formatter)

    logger.addHandler(target_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connection to MySQL environment """
    db_connect = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME', '')
    )
    return db_connect


def main() -> None:
    """connect to the database, retrieve data"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")

    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[HOLBERTON] %(name)s %(levelname)s %(asctime)s: %(message)s',
        "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    rows = cursor.fetchall()
    for row in rows:
        log_msg = '; '.join([f"{key}={value}" for key, value in row.items()])
        filtered_msg = filter_datum(PII_FIELDS, '***', log_msg, '; ')
        logger.info(filtered_msg)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
