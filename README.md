# Assortment of python code
bond_stuff_in_progress.py contains the most up to date code.
The parsing functions simply point at publicly available 
bond information from the previous day's close.

##bond_stuff_in_progress.py includes functions that:
* Create a portfolio from a CSV of bonds
* Value single bonds given bond charachteristics
* Value a portfolio of bonds
* Calculate the duration and Modified duration for a single bond given bond charachteristics
* Calculate the duration and Modified duration for a portfolio  of bonds
* Calculate the convexity for a single bond given bond charachteristics
* Calculate the convexity for a portfolio of bonds
* Calculates the Value at Risk for a single bond (Work in progress)
* Calculates the Value at Risk for a portfolio of bonds (Work in progress)
* And several other functions that help to perform the above calculations
* **Further development necessary to handle translations to and from foreign currencies**

##html_parsing_us_strips_data.py is a single function that:
* Downloads the prior trading day's yields for US Treasury STRIPS of all trading maturities, inserts those STRIPS yields into an .xlsx and generates a yield curve from the STRIPS maturity dates and yields.

##xml_parsing_strips_data.py is a single function that:
* Downloads the prior trading day's yields for UK Gilt STRIPS of all trading maturities, inserts those STRIPS yields into an .xlsx and generates a yield curve from the STRIPS maturity dates and yields.

**The remaining files are simply precursors to bond_stuff_in_progress.py**