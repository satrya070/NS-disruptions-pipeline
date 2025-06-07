import boto3
import psycopg2
import os
import duckdb
import pandas as pd
import logging

MONITORING_DB = "monitoring.db"


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
            # fetch all queries that were run and their executing time
            sql_queries_info = """
                SELECT
                    query, calls, total_exec_time, mean_exec_time, rows, DATE_TRUNC('minute', NOW()) AS recording_date
                FROM pg_stat_statements
                WHERE userid = '24278983'
                ORDER BY mean_exec_time DESC;"""
            cursor.execute(sql_queries_info)
            queries_info_data = cursor.fetchall()

            # fetch the used disk space of the database
            sql_database_size = "SELECT pg_database_size('bnu1cjzmuwmm6xysyc9z'), DATE_TRUNC('minute', NOW()) AS recording_date;"
            cursor.execute(sql_database_size)
            database_size_data = [cursor.fetchone()]

            # fetch the size of all tables and materialized views
            sql_tables_sizes = """
            SELECT
                relname AS table, pg_total_relation_size(relid) AS table_size_bytes, date_trunc('minute', now()) AS recording_date
            FROM pg_catalog.pg_statio_user_tables
            WHERE schemaname = 'ns'
            ORDER BY pg_total_relation_size(relid) DESC;
            """
            cursor.execute(sql_tables_sizes)
            tables_sizes_data = cursor.fetchall()

            # download duckdb from s3
            s3_client = boto3.client("s3")
            s3_client.download_file("ns-disruptions", f"monitoring/{MONITORING_DB}", f"/tmp/{MONITORING_DB}")
            
            # update duck db table
            duckconn = duckdb.connect(f"/tmp/{MONITORING_DB}")

            # insert all monitor data in duckdb
            duckconn.executemany("INSERT INTO queries_info VALUES(?, ?, ?, ?, ?, ?)", queries_info_data)
            duckconn.executemany("INSERT INTO database_size VALUES(?, ?)", database_size_data)
            duckconn.executemany("INSERT INTO table_sizes VALUES(?, ?, ?)", tables_sizes_data)
            duckconn.close()

            print("duckdb succesfully updated with monitoring data.")

            # upload updated duck db
            s3_client.upload_file(f"/tmp/{MONITORING_DB}", "ns-disruptions", f"monitoring/{MONITORING_DB}")
            print("duckdb succesfully uploaded to s3.")

    except Exception as e:
        logging.error(e)
        raise e
    
    finally:
        # make sure pg conn closes regardless of exceptions
        conn.close()