

def process_spaces(coin: str) -> str:
    if " " not in coin:
        return coin

    # coin name has spaces so interleave with space (%20)
    name_parts = coin.split(" ")
    coin_processed = "%20".join(name_parts)

    return coin_processed