import boto3
import psycopg2
import os
import duckdb
import pandas as pd
import logging

def monitor_db():
    """
    executes monitoring queries on the postgres db and update the monitoring duckdb on s3
    """
    conn = psycopg2.connect(
        host=os.environ["PGHOST"],
        port=os.environ["PGPORT"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        dbname=os.environ["PGDATABASE"]
    )

    try:
        with conn.cursor() as cursor:
            # fetch monitoring data tables
            sql_queries_info = """
                SELECT
                    query, calls, total_exec_time, mean_exec_time, rows
                FROM pg_stat_statements
                WHERE userid = '24278983'
                ORDER BY mean_exec_time DESC;"""
            cursor.execute(sql_queries_info)
            queries_info_data = cursor.fetchall()

            sql_database_size = "SELECT pg_size_pretty(pg_database_size('bnu1cjzmuwmm6xysyc9z'));"
            cursor.execute(sql_database_size)
            database_size_data = cursor.fetchone()

            # download duckdb from s3
            #s3_client = boto3.client("s3")
            #s3_client.download_file()
            
            # update duck db table
            duckconn = duckdb.connect("/tmp/test.db")

            # TODO insert datatime
            duckconn.executemany("INSERT INTO queries_info VALUES(?, ?, ?, ?, ?)", queries_info_data)
            duckconn.executemany("INSERT INTO database_size VALUES(?)", list(database_size_data))
            # duckconn.executemany("INSERT INTO table_sizes VALUES(?, ?, ?, ?, ?)", queries_info)
            duckconn.close()

            # upload updated duck db

        conn.close()

    except Exception as e:
        logging.error(e)
        raise e
