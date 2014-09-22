Spam Filter
===========
Descrition:
------------
	It is a spam filter to distinguish between spam and ham emails effectively

Distribution Structure:
-----------------------
* conf.py : All the configuration related constants are defined here
* stopwords_en.txt : List of english language stopwords
* utils.py : Utility functions used by spam filter for reading data from file, writing data into file, dividing data into different folders as per label and generating KFold data
* text_processing.py : Functions for preprocessing the data and give back list of tokens
* spam_filter.py : Train, test, classify functions for spam filter
	
Usage:
------
1. Define configuration related constants in conf.py
2. Run the script as:
    python spam_filter.py
	  
