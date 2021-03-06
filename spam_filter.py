import os
from collections import defaultdict

from nltk import NaiveBayesClassifier
import nltk.classify

import conf
import utils
import text_processing

def get_features(mail, **kwargs):
	'''
	Returns a dictionary of {word: freq} for all words in mail
	'''
	features = defaultdict(list)
	mail_words = text_processing.get_words(mail, **kwargs)
	for word in mail_words:
		features[word] = True 
	return features

def get_features_label(mails, label, **kwargs):
	'''
	Extract features from all given mails with label (spam/ham)
	'''
	features_labels = []
	for mail in mails:
		features = get_features(mail, **kwargs)
		features_labels.append((features, label))
	return features_labels

def process_train_data(spam_mails, ham_mails, **kwargs):
	'''
	Process the content of e-mails and divide it in given no of parts
	'''
	spam = get_features_label(spam_mails, 0, **kwargs)
	ham = get_features_label(ham_mails, 1, **kwargs)
	return spam, ham

def get_matrix(spam_set, ham_set, num_folds):
	'''
	Generate different matrix by taking the average of K Fold data
	'''
	total_precision = total_recall = F1 = spam_accuracy = ham_accuracy = 0

	for train_set, test_spam_set, test_ham_set in utils.get_kfold_data(spam_set, ham_set, num_folds):
		classifier = NaiveBayesClassifier.train(train_set)
		spam_len = len(test_spam_set)
		ham_len = len(test_ham_set)
		true_positive = false_positive = true_negative = false_negative = 0
		for test in test_spam_set:
			features = test[0]
			predicted_label = classifier.classify(features)
			if predicted_label == 0:
				true_positive += 1
			else:
				false_negative += 1
		for test in test_ham_set:
			features = test[0]
			predicted_label = classifier.classify(features)
			if predicted_label == 1:
				true_negative += 1
			else:
				false_positive += 1
												
		precision = true_positive / float(true_positive + false_positive)
		recall = true_positive / float(true_positive + false_negative)
		F1 += (2 * precision * recall) / (precision + recall)
		spam_accuracy += true_positive / float(true_positive + false_negative)
		ham_accuracy += true_negative / float(true_negative + false_positive)
		total_precision += precision
		total_recall += recall

	return total_precision/num_folds, total_recall/num_folds, F1/num_folds, spam_accuracy*100/num_folds, ham_accuracy*100/num_folds

def classify_data(classifier, test_mails, **kwargs):
	'''
	Classify the data and generates line correspoding to each mail
	'''
	for mail in test_mails:
		mail_content = mail[0]
		filename = mail[1]
		features = get_features(mail_content, **kwargs)
		label = classifier.classify(features)
		yield str(label) + " " + filename + "\n"

def main():    	
	# Extract list of stopwords
	with open(conf.STOPWORDS_FILE, 'r') as f:
		stopword_list = f.read()
		sw = set([w.strip() for w in stopword_list.split()])
		
	# Split data into ham and spam folders
	train_data_path = os.path.abspath(os.path.join(conf.TRAIN_DIR))
	train_file_path = os.path.abspath(os.path.join(conf.TRAIN_FILE))
	utils.split_data(train_file_path, train_data_path)

	# Process training data and prepare sets of (features, label) data
	spam_path = os.path.join(train_data_path, '0')     # label 0 for spam
	ham_path = os.path.join(train_data_path, '1') 	  # label 1 for ham
	spam_mails = utils.get_dir_data(spam_path)
	ham_mails = utils.get_dir_data(ham_path)	
	spam_set, ham_set = process_train_data(spam_mails, ham_mails, stopwords = sw)

	# 5 Fold Cross Validation with training data to report result metrics
	precision, recall, F1, ham_mails_accuracy, spam_mails_accuracy = \
	get_matrix(spam_set, ham_set, conf.NUM_FOLDS)
	print "Precision : %.4f" % precision 
	print "Recall : %.4f" % recall
	print "F1 : %.4f" % F1
	print "Spam Mails Accuracy : %.2f" % spam_mails_accuracy 
	print "Ham Mails Accuracy : %.2f" % ham_mails_accuracy

	# Model training on 100% train data
	train_set = spam_set + ham_set
	classifier = NaiveBayesClassifier.train(train_set)

	# Top 20 informative features
	print classifier.show_most_informative_features(20)

	# Classify on given test data
	test_data_path = os.path.abspath(os.path.join(conf.TEST_DIR))
	output_dir_path = os.path.abspath(os.path.join(conf.OUTPUT_DIR))	
	if not os.path.exists(output_dir_path):
		os.makedirs(output_path)
	output_file_path = os.path.join(output_dir_path, conf.OUTPUT_FILE)
	test_mails = utils.get_dir_data_with_filename(test_data_path)
	utils.write_file(output_file_path, classify_data(classifier, test_mails, stopwords = sw))

if __name__ == '__main__':
	main()


