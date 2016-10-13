# Assortment of python code
The parsing functions simply point at publicly available 
bond information from the previous day's close.
The bond_class.py and portfolio_class.py files are the 
most up to date code for the bond functions, 
older files have been moved to the old_code directory.

##bond_functions includes classes with methods that:
* Create a portfolio from a CSV of bonds
* Create a portfolio by querying a PostgreSql database
* Value single bonds given bond charachteristics
* Value a portfolio of bonds
* Calculate the duration and Modified duration for a single bond given bond charachteristics
* Calculate the duration and Modified duration for a portfolio  of bonds
* Calculate the convexity for a single bond given bond charachteristics
* Calculate the convexity for a portfolio of bonds
* Calculates the Value at Risk for a portfolio of bonds using historical yield curve shifts
	* Allows selection of VaR percentile of loss, size of historical returns subsample, and the time horizon in days for the VaR
* And several other functions that help to perform the above calculations
* **Further development necessary to handle translations to and from foreign currencies**

##tests includes:
* Tests for bond_class.py with bounded validity to allow for daily changes in yields
* Tests for portfolio_class.py with bounded validity to allow for daily changes in yields

##parsing_functions includes:
html_parsing_us_strips_data.py is a single function that:
* Downloads the prior trading day's yields for US Treasury STRIPS of all trading maturities,inserts those STRIPS yields into an .xlsx and generates a yield curve from the STRIPS maturity dates and yields. Also generates and plots a continuous yield curve by interpolating between maturity dates by using a cubic spline.

xml_parsing_strips_data.py is a single function that:
* Downloads the prior trading day's yields for UK Gilt STRIPS of all trading maturities, inserts those STRIPS yields into an .xlsx and generates a yield curve from the STRIPS maturity dates and yields. Also generates and plots a continuous yield curve by interpolating between maturity dates by using a cubic spline.

##countdown_code includes:
* a script that inputs letters and returns the longest (min 5 letters) words that can be created with those letters by scanning a dictionary.
* Different dictionary files return different results; I have yet to find an all encompassing, freely-available English dictionary.
**The remaining files are simply precursors to bond_stuff_in_progress.py**

## webscraping includes:
* A function that inputs query parameters and performs a query through the webhose.io API
* A function that iterates through the results of the webhose.io API, extracts pertinent page content, and passes the distilled page content to the TextRazor API for analysis, finally returning metadata of the analysis
* Sample Outputs of the processes outlined above

## yahoo_finance_code includes:
* A script for misc testing of the yahoo finance API
