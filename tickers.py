def getTickers() -> list[str]:
    tickers = list()

    with open("list.txt", "r") as file:
        for line in file:
            line = line.replace("\n", "")
            tickers.append(line)

    return tickers