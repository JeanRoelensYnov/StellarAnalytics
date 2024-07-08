from StellarAnalytics.Data import Formatter, Scrapper, Requests_tools
from pprint import pprint
if __name__ == "__main__":
    # Data retrieving and CSV Creation logic.
    urlDict = Scrapper.url_builder()
    for symbol, url in urlDict.items():
        table = Scrapper.get_table(Requests_tools.req(url))
        tBody = Scrapper.get_tbody(table)
        observedWavelength, relativeIntensities = Scrapper.get_tbody_content(tBody)
        if len(observedWavelength) > 0 and len(relativeIntensities) > 0:
            Formatter.createCSV(observedWavelength, relativeIntensities, symbol)
