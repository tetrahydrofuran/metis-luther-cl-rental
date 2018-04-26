## Craigslist Apt/Home Rental Linear Regression Model

A utility that is capable of scraping Craigslist search results, and apartment/home rental results specifically.
The scraped data is used to fit a linear regression model, and plots evaluating the efficacy of the model are generated.

------
### Getting Started

With Python installed and configured, the `bin/main.py` file may be run directly.  The target URLs and depth of scraping may easily be modified to gather more or less data.
#### Required Libraries
If any libraries are missing, they may be easily installed with the command `pip install --upgrade [library]`.
* `pandas`
* `numpy`
* `sklearn`
* `matplotlib`
* `scipy`
* `requests`
* `bs4`
------

#### Repository Structure
* `bin`: Contains scripts to run, including the entry point, `main.py`.
* `data`: Directory for saved CSV files to be generated, and where `main.py` will expect to find data to import.
* `img`: Saved plots generated by the program.
