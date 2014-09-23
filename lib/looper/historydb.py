#!/usr/bin/python2
import sqlite3
import os,fnmatch,time

data_create_stmt = '''
CREATE TABLE IF NOT EXISTS data
(
    idx         INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    compression INTEGER NOT NULL,
    raw_req     BLOB NOT NULL,
    raw_resp    BLOB NOT NULL
)'''

metadata_create_stmt = '''
CREATE TABLE IF NOT EXISTS metadata
(
    idx             INTEGER NOT NULL UNIQUE PRIMARY KEY,
    proto           TEXT,
    netloc          TEXT,
    method          TEXT,
    path            TEXT,
    t_connect       REAL NOT NULL,
    t_duration      REAL NOT NULL,
    sockerror       TEXT,
    FOREIGN KEY(idx) REFERENCES data(idx)
)'''

header_create_stmt = '''
CREATE TABLE IF NOT EXISTS headers
(
    idx             INTEGER NOT NULL,
    header          TEXT,
    value           TEXT,
    FOREIGN KEY(id) REFERENCES data(idx)
)

CREATE INDEX index_name ON table_name (header)
CREATE INDEX index_name ON table_name (value)
'''

metadata_insert_stmt = '''
INSERT INTO metadata 
(
    idx,
    proto,
    netloc,
    sockerror,
    t_connect,
    t_duration,
    method,
    path
) VALUES (?,?,?,?,?,?,?,?)
'''

class historydb():
    def __init__(self,path):
        self.db = sqlite3.connect(path)
        c = self.db.cursor()
        c.execute(data_create_stmt)
        c.execute(metadata_create_stmt)
        c.close()
        self.db.commit()

    def add_metadata(self,idx,proto,netloc,sockerror,t_connect,t_duration,method,path):
        c = self.db.cursor()
        c.execute(metadata_insert_stmt,(idx,proto,netloc,sockerror,t_connect,t_duration,method,path))
        c.close()

    def add_data(self,req,resp):
        c = self.db.cursor()
        c.execute("INSERT INTO data (compression,raw_req,raw_resp) VALUES (?,?,?)",(0,sqlite3.Binary(req),sqlite3.Binary(resp)))
        idx = c.lastrowid
        c.close()
        return idx

    def add_entry(self,proto,netloc,sockerror,t_connect,t_duration,method,path,req,resp):
        idx = self.add_data(req,resp)
        self.add_metadata(idx,proto,netloc,sockerror,t_connect,t_duration,method,path)
        return idx

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.commit()
        self.db.close()


