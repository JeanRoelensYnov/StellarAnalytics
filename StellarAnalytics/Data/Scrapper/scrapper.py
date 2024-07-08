from bs4 import BeautifulSoup
from requests.models import Response
from ..Requests_tools import request_tools
from locale import atof

def url_builder() -> dict:
    """
    Get the common start and end of url necessary for data retrieving, then buil url by concatenation with
    the chemical symbol and ionization like this : START_URL + SYMBOL + IONIZATION + END_URL.
    Return a dict with SYMBOL IONIZATION as key and CONCATENATED_URL as value.
    """
    resp = {}
    sUrl, eUrl, eDict = request_tools.load_const()
    for key in eDict.keys():
        for v in eDict[key]:
            resp[key+" "+ v] = sUrl + key + "+" + v + eUrl
    return resp

def get_table(req : Response):
    """
    Parser help to get the correct table containing the data in which we are interested in.
    """
    soup = BeautifulSoup(req.text,'html.parser')
    tables = soup.find_all('table')
    targetTable = [table for table in tables if 'background-color:#FFFEEE;' in table.get('style', '')]
    if len(targetTable) > 0:
        return targetTable[0]
    else:
        return None

def get_tbody(table):
    """
    Parser help to get the correct tbody containing the data in which we are interested in.
    """
    return table.find_all('tbody')[1]

def get_tbody_content(tbody) -> tuple[list, list]:
    """
    Mashup of all the scrapper logic, for a given tbody will return a tuple containing two list the first one
    being the observed wavelength and the second list is realtive intensities.
    """
    observedWavelength = []
    relativeIntensities = []
    for tr in tbody.find_all('tr'):
        allTd = tr.find_all('td')
        if len(allTd) >= 2:
            try:
                wavelength = atof(allTd[0].text.strip())
                intensities = atof(allTd[2].text.strip())
                if wavelength != None and intensities != None:
                    observedWavelength.append(wavelength)
                    relativeIntensities.append(intensities)
            except ValueError:
                continue
    return observedWavelength,relativeIntensities


