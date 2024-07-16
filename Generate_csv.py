from StellarAnalytics.Data import Formatter, Scrapper, Requests_tools

if __name__ == "__main__":
    urlDict = Scrapper.url_builder()
    for symbol, url in urlDict.items():
        idx = Scrapper.get_idx_relInt(Requests_tools.req(url))
        table = Scrapper.get_table(Requests_tools.req(url))
        tBody = Scrapper.get_tbody(table)
        observedWavelength, relativeIntensities = Scrapper.get_tbody_content(tBody, idx)
        if len(observedWavelength) > 0 and len(relativeIntensities) > 0:
            Formatter.createCSV(observedWavelength, relativeIntensities, symbol)