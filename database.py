import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='MetaFit',
        user='postgres',
        password='senai'
    )
    return conn


def get_db_cursor(conn):
    """Retorna um cursor que retorna dicionários"""
    return conn.cursor(cursor_factory=RealDictCursor)
