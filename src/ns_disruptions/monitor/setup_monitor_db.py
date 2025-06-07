import duckdb
import argparse
import logging


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a duckdb in /tmp with all monitoring tables with a given name.")
    parser.add_argument("--name", required=True, type=str)
    args = parser.parse_args()

    db_name = args.name
    duckconn = duckdb.connect(f"/tmp/{db_name}.db")

    try:
        # create all the monitoring tables
        duckconn.sql("CREATE TABLE queries_info (query TEXT, calls INTEGER, total_exec_time FLOAT, mean_exec_time FLOAT, rows INTEGER);")
        duckconn.sql("CREATE TABLE database_size (size_bytes INTEGER);")

        duckconn.close()
    except Exception as e:
        print(e)

    print(f"duckdb `/tmp/{db_name}.db` succesfully created")