def getTickers(path: str) -> list[str]:
    tickers = list()

    with open(path, "r") as file:
        for line in file:
            line = line.replace("\n", "")
            tickers.append(line)

    return tickers
