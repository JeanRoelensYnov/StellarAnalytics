import requests
import yaml
from pathlib import Path
"""
Some rule to follow for me (Jean) :
variables in camel case example :aVarVeryImportant
function in snake case example : some_function_useful
and constant in pascal case example : SomethingWhichIsConstant

Following the rules of clean code your functions shouldn't exceed 25 lines
"""
def load_const() -> tuple[str, str, dict]:
    """
    Loader for parameter present in our config.yml file.
    """
    configPath = Path(__file__).parent.parent / 'config.yml'
    if not configPath.is_file():
        raise FileNotFoundError(f"Config file not found at: {configPath}")
    
    with open(configPath,'r') as f:
        content = yaml.safe_load(f)
    sUrl = content['start_url']
    eUrl = content['end_url']
    eDict = content['element_dict']
    return sUrl, eUrl, eDict

def req(URL) -> requests.models.Response:
    """
    QOL function to retrieve requests response.
    """
    return requests.get(URL)

def test_url(URL) -> bool:
    """
    Safeguard to check if a URL is correctly formatted or if it doesn't return a status code other than 200.
    """
    if req(URL).status_code == 200 :
        return True
    return False
