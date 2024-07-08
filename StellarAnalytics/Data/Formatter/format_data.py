import pandas as pd
from pathlib import Path

def createCSV(wavelength,relativeIntensities,symbol):
    """
    CSV creation logic function for correct data output.
    """
    outputDir = Path(__file__).parent.parent / 'Output'
    outputDir.mkdir(parents=True,exist_ok=True)
    csvPath = outputDir/f'{symbol}.csv'
    df = pd.DataFrame({"wavelength" : wavelength, "relint" : relativeIntensities})
    df.to_csv(csvPath, index=False, encoding="UTF-8")
