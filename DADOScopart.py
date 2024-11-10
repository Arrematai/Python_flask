import os
import sys
import sqlite3
import pandas as pd

class DBStorage():
    def __init__(self):
        self.con= sqlite3.connect("Porsche.db")

        self.setup_tables()


    def setup_tables(self):
        cur =self.con.cursor()
        #ID = lote ; query=  ; rank=  ;snippet=
        results_table = r"""
            CREATE TABLE IF NOT EXISTS results (
            ID INTEGER PRIMARY KEY,
            lote INTEGER, 
            query TEXT,
            rank INTEGER,
            link TEXT,
            marca TEXT,
            modelo TEXT,
            monta TEXT,
            ano INTEGER,
            title TEXT,
            snippet TEXT,
            html TEXT,
            created DATETIME,
            relevance INTEGER,
            UNIQUE (query, link)            
            );
        """
        cur.execute(results_table)
        self.con.commit()
        cur.close()

    def query_results(self,query):
        df = pd.read_sql(f"select * from results where query='{query}' order by rank asc;", self.con)
        return df

    def insert_row(self,values):
        cur = self.con.cursor()
        try:
            cur.execute('INSERT INTO results (query, rank, link, title, snippet, html, created) VALUES(?, ?, ?, ?, ?, ?, ?)', values)
            self.con.commit()
        except sqlite3.IntegrityError:
            pass
        cur.close()


