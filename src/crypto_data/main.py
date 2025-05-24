from crypto_data.etl import extract_data, load_data

def main():
    coin_api_data: dict[str, dict] = extract_data()
    load_data(coin_api_data)


if __name__ == "__main__":
    main()