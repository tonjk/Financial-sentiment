# Financial-sentiment

* Overview of Data

There are 1,596 folders. Each folder is numbered (i.e. 1045, 1075, 1076, etc.), these are company
identifier numbers and should be labeled as the variable name ‘GVKEY’ for each company in the .csv
or .xlsx output file. These company identifier numbers are important for pulling in financial data, etc.
in later analysis. Each folder (each company), has multiple .rtf files with news articles from multiple
sources based on my filters and ranged between 1/1/2020 to 1/11/2021. Each article is separated by
a unique document number (i.e. Document LBA0000020200102eg12023p1 and Document
RSTPROCY20200102eg120002t for the first two articles for the company ‘1045’).

* Objective

Each article will become each individual observation. Python will be required to read through each
article and determine whether the sentiment is positive or negative based on the text analysis in the
article for each company (based on discussion with Aj Pree). This can be a 1/0 binary variable or a
continuous variable between 0 and 1 (degree of positivity). Whichever is possible is fine.