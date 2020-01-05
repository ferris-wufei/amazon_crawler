# -*- coding: utf-8 -*-
from ambot import AMBot
from mysql_connector import MySQL
import os
import logging
import logging.config
_current_dir = os.path.dirname(os.path.realpath(__file__))
logging.config.fileConfig(os.path.join(
    _current_dir, 'logging.conf'), disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def main():
    
    with MySQL(**_config) as ms:
        ms.query("select asin from test.asin;")
        asin_list = (i[0] for i in ms.fetch())
    
    bot = AMBot()
    listing_info = list()
    
    for a in asin_list:
        l = bot.get_product_info(a)
        if l != None:
            listing_info.append(l)

    with MySQL(**_config) as ms: 
        for li in listing_info:
            tbl_str = "test.product_info"
            val_str = "(" + ", ".join(["%s"] * len(li)) + ")"
            col_str = "(" + ", ".join(li.keys()) + ")"
            stmt = f"insert into {tbl_str} {col_str} values {val_str};"
            values = tuple(str(i) for i in li.values())
            logger.info(f"values: {values}")
            ms.insert(stmt, values)


if __name__ == "__main__":

    # for test on local machine
    _config = {
        'user': 'root',
        'password': '<your_password>',
        'host': '127.0.0.1',
        'raise_on_warnings': True
        }

    main()
