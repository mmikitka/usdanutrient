# Requirements
* >=Python 2.7
* SQLAlachemy Python package

# Importing USDA Nutritional Data
The USDA nutritional data source data files are stored in the data directory of this repository. The following database versions are supported:
* [SR28](https://www.ars.usda.gov/Services/docs.htm?docid=25700)

Follow these steps to import the source data files into a destination database of your choice:

1. `cp conf/usdanutrient.yml.example conf/usdanutrient.yml`
1. Modify the database connection string in conf/usdanutrient.yml
1. `bin/usdanutrient import`
