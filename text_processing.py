import re
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import PorterStemmer
	
def get_words(data, stopwords = []):
	'''
	preprocesses and tokenise any data and returns a list of words  
	'''	
	# Lower case
	#data = str.lower(data);
	
	# Strip all html tags and attributes and html character codes, like &nbsp; and &lt;
	data = re.sub('<(.|\n)*?>', ' ', data)
	data = re.sub('&\w+;', ' ', data)
	
	# Handle URLS (Look for strings starting with http:// or https://)
	#data = re.sub('(http|https)://[^\s]*', ' httpaddr ', data)

	# Handle Email Addresses (Look for strings with @ in the middle)
	#data = re.sub('[^\s]+@[^\s]+', ' emailaddr ', data);

	# Handle $ sign
	data = re.sub('[$]+', ' dollar ', data)	
	
	# Strip out weird '3D' artefacts.
	data = re.sub('3D', ' ', data)

	# Replace multiple underscores with a single one
	data = re.sub('_+', '_', data)

	# Remove '=' symbols before tokenizing, since these are sometimes occur within words to indicate, e.g., line-wrapping
	data = data.replace('=\n', '')

	# Tokenize Edata
	data_words = wordpunct_tokenize(data)

	# Get rid of stopwords
	#data_words = [w for w in data_words if w not in stopwords]
		      
	# Remove any non alphanumeric characters
	data_words = map(lambda word:re.sub('[^a-zA-Z0-9]', '', word), data_words)

	# Get rid of punctuation tokens, numbers and single letters
	data_words = [w for w in data_words if re.search('[a-zA-Z]', w) and len(w) > 1]	

	# Stemming of words
	#data_words = map(lambda word:PorterStemmer().stem_word(unicode(word, errors='replace')), data_words)	

	return data_words

