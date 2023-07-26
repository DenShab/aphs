import sqlite3
from sqlite3 import Error
import configparser
import os
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, 'config')
print(config_path)
config = configparser.ConfigParser()
config.read(config_path)
path1 = config.get('config', 'pathbd')
bd_path = os.path.join(application_path, path1)
print(bd_path)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)





def main():
    sql_create_section = """
        CREATE TABLE section (
            section TEXT NOT NULL UNIQUE
        );
        """
    sql_create_doc = """
    CREATE TABLE doc (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        section TEXT NOT NULL,
        non_format_text TEXT UNIQUE,
        format_text TEXT,
        links TEXT
    );
    """
    doc_fts = """
    CREATE VIRTUAL TABLE doc_fts USING fts5(
        name, 
        non_format_text, 
        section UNINDEXED, 
        content='doc', 
        content_rowid='id' 
    );
    """
    doc_fts_config = "CREATE TABLE 'doc_fts_config'(k PRIMARY KEY, v) WITHOUT ROWID;"
    doc_fts_data = "CREATE TABLE 'doc_fts_data'(id INTEGER PRIMARY KEY, block BLOB);"
    doc_fts_docsize = "CREATE TABLE 'doc_fts_docsize'(id INTEGER PRIMARY KEY, sz BLOB);"
    doc_fts_idx = "CREATE TABLE 'doc_fts_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID;"
    doc_ai = """
    CREATE TRIGGER doc_ai AFTER INSERT ON doc
        BEGIN
            INSERT INTO doc_fts (rowid, name, non_format_text)
            VALUES (new.id, new.name, new.non_format_text);
            INSERT OR REPLACE INTO section (section)
            VALUES (new.section);
        END;
    """
    doc_ad = """
    CREATE TRIGGER doc_ad AFTER DELETE ON doc
        BEGIN
            INSERT INTO doc_fts (doc_fts, rowid, name, non_format_text)
            VALUES ('delete', old.id, old.name, old.non_format_text);
        END;
    """
    doc_au = """
    CREATE TRIGGER doc_au AFTER UPDATE ON doc
        BEGIN
            INSERT INTO doc_fts (doc_fts, rowid, name, non_format_text)
            VALUES ('delete', old.id, old.name, old.non_format_text);
            INSERT INTO doc_fts (rowid, name, non_format_text)
            VALUES (new.id, new.name, new.non_format_text);
        END;
    """
#CREATE VIRTUAL TABLE table_name USING FTS5(column1, column2...);
    sql_create_doc_table = """ CREATE VIRTUAL TABLE IF NOT EXISTS DocFTS5 USING fts5(
                                        name,
                                        non_format_text,
                                        format_text,
                                        links,
                                        section); """

    # create a database connection
    conn = create_connection(bd_path)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_section)
        create_table(conn, sql_create_doc)
        create_table(conn, doc_fts)
        create_table(conn, doc_fts_config)
        create_table(conn, doc_fts_data)
        create_table(conn, doc_fts_docsize)
        create_table(conn, doc_fts_idx)
        create_table(conn, doc_ai)
        create_table(conn, doc_ad)
        create_table(conn, doc_au)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
