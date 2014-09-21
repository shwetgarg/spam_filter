import os
import random

def get_kfold_data(spam_set, ham_set, num_folds):
    '''
    Divides all the samples in k = num_folds groups of samples of approximately equal sizes. The prediction function is learned using k - 1 folds, and the fold left out is used for test.
    '''
    random.shuffle(spam_set)
    random.shuffle(ham_set)
    spam_chunk_size = len(spam_set)/num_folds
    ham_chunk_size = len(ham_set)/num_folds
    for i in range(num_folds):
        test_spam_set = spam_set[i*spam_chunk_size:(i+1)*spam_chunk_size]
        train_spam_set = spam_set[:i*spam_chunk_size] + spam_set[(i+1)*spam_chunk_size:]
        test_ham_set = ham_set[i*ham_chunk_size:(i+1)*ham_chunk_size]
        train_ham_set = ham_set[:i*ham_chunk_size] + ham_set[(i+1)*ham_chunk_size:]
        yield (train_spam_set + train_ham_set, test_spam_set, test_ham_set)

def get_file_data(path):
    '''
    Read content of a file and return
    '''    
    with open(path, 'rb') as f:
        data = f.read()
        return data        

def get_dir_data(path):
    '''
    Read and return content of all files in a directory
    '''    
    filelist = os.listdir(path)
    data = [get_file_data(os.path.join(path, f)) for f in filelist]
    return data

def get_dir_data_with_filename(path):
    '''
    Read and return content of all files in a directory with filename
    '''    
    filelist = os.listdir(path)
    data = [(get_file_data(os.path.join(path, f)), f) for f in filelist]
    return data

def write_file(filename, iterator):
    '''
    Write content of iterator in given file
    '''
    with open(filename, 'wb') as f:
        for line in iterator:
            f.write(line)

