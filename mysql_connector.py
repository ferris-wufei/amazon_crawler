# -*- coding: utf-8 -*-
import mysql.connector
import logging
logger = logging.getLogger(__name__)

class MySQL:

    def __init__(self, **kwargs):
        logger.info("connecting to MySQL")
        self.cnx = mysql.connector.connect(**kwargs)
        self.cursor = self.cnx.cursor()

    def __enter__(self):
        return self

    def __exit__(self, 
        exception_type, exception_value, traceback):
        self.cnx.commit()
        if self.cnx:
            self.cnx.close()

    def query(self, query: str) -> None:
        logger.info(f"executing query: {query}")
        self.cursor.execute(query)

    def fetch(self) -> list:
        res = list()
        logger.info("retrieving query results")
        for r in self.cursor:
            logger.debug(f"query result: {r}")
            res.append(r)
        return res

    def insert(self, stmt: str, data: tuple) -> None:
        logger.debug(f"inserting data {str(data)}")
        self.cursor.execute(stmt, data)
