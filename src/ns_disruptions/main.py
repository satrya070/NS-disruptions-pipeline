from ns_disruptions.etl import ETL


def main():
    etl_processor = ETL()
    extracted_data = etl_processor.extract_data()
    transformed_data = etl_processor.transform_data()

if __name__ == "__main__":
    main()