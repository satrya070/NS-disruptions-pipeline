from ns_disruptions.etl import ETL
from ns_disruptions.monitor.monitor import monitor_db


def main():
    etl_processor = ETL()
    extracted_data = etl_processor.extract_data()
    transformed_data = etl_processor.transform_data(extracted_data)
    etl_processor.load_data(transformed_data)
    etl_processor.refresh_data_views()

    #monitor_db()


if __name__ == "__main__":
    # main()
    monitor_db()