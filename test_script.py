from StellarAnalytics.Data import Formatter, Scrapper, Requests_tools
import pandas as pd
from pprint import pprint
if __name__ == "__main__":
    # Data retrieving and CSV Creation logic.
    urlDict = Scrapper.url_builder()
    for symbol, url in urlDict.items():
        idx = Scrapper.get_idx_relInt(Requests_tools.req(url))
        table = Scrapper.get_table(Requests_tools.req(url))
        tBody = Scrapper.get_tbody(table)
        observedWavelength, relativeIntensities = Scrapper.get_tbody_content(tBody, idx)
        if len(observedWavelength) > 0 and len(relativeIntensities) > 0:
            Formatter.createCSV(observedWavelength, relativeIntensities, symbol)
    # test = "https://physics.nist.gov/cgi-bin/ASD/lines1.pl?spectra=NA+V&output_type=0&low_w=&upp_w=&unit=1&submit=Retrieve+Data&de=0&plot_out=0&I_scale_type=1&format=0&line_out=0&en_unit=0&output=0&bibrefs=1&page_size=15&show_obs_wl=1&show_calc_wl=1&unc_out=1&order_out=0&max_low_enrg=&show_av=2&max_upp_enrg=&tsb_value=0&min_str=&A_out=0&intens_out=on&max_str=&allowed_out=1&forbid_out=1&min_accur=&min_intens=&conf_out=on&term_out=on&enrg_out=on&J_out=on"
    # idxRelInt = Scrapper.get_idx_relInt(Requests_tools.req(test))
    # table = Scrapper.get_table(Requests_tools.req(test))
    # tBody = Scrapper.get_tbody(table)
    # observedWavelength, relativeIntensities = Scrapper.get_tbody_content(tBody, idxRelInt)
    # if len(observedWavelength) > 0 and len(relativeIntensities) > 0:
    #         Formatter.createCSV(observedWavelength, relativeIntensities, "testResult")

