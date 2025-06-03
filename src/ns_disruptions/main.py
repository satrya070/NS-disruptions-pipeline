from ns_disruptions.etl import ETL


def main():
    etl_processor = ETL()
    extracted_data = etl_processor.extract_data()
    transformed_data = etl_processor.transform_data(extracted_data)
    etl_processor.load_data(transformed_data)
    etl_processor.refresh_data_views()


if __name__ == "__main__":
    main()