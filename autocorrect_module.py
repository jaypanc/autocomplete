import re
from collections import Counter
import numpy as np
import pandas as pd

def process_data(file_name):
    """
    Input:
        file_name: just a file to read 
    Output:
        wrods: list containing all words of file in lower case
    """

    words=[]

    with open(file_name) as f:
        file_name_data = f.read()

    file_name_data = file_name_data.lower()
    words = re.findall("\w+",file_name_data)

    return words


def get_count(word_l):
    """
    Input: 
        word_l : list of all words read from text file
    Output:
        word_count_dict: dictionary where key is word and value is frequency
    """
    
    word_count_dict = {}
    for word in word_l:
        if word in word_count_dict.keys():
            word_count_dict[word]+=1
        else:
            word_count_dict[word]=1
    
    return word_count_dict


def get_prob(word_count_dict):
    """
    Input: 
        word_count_dict: dictionary of words as key and frequency as values
    Output:
        probs: dictionary with key as word and value as probability
    """

    probs={}
    
    total_count_words = sum(word_count_dict.values())

    for word in word_count_dict.keys():
        probs[word] = word_count_dict[word]/total_count_words
    
    return probs

def delete_letter(word,verbose=False):
    """
    Input:
        word: word for which you will generate all possible words in vocab which have 1 missing character
    Output:
        delete_l: a list of all possible words obtained by deleting 1 character
    """

    splits_l = [(word[:i],word[i:]) for i in range(len(word)+1)]

    delete_l = [L+R[1:] for L,R in splits_l if R]
    
    if verbose:
        print(f"input word = {word}\nsplits_l = {splits_l}\ndelete_l = {delete_l}")

    return delete_l


def switch_letter(word,verbose=False):
    """
    Input:  
        word:   word for which you will generate all possible words in vocab by switching 1 character
    Output:
        switch_l:   list of all possible words obtained by switching 1 character
    """

    splits_l =[(word[:i],word[i:]) for i in range(len(word)+1)]

    switch_l =[L+R[1]+R[0]+R[2:] for L,R in splits_l if len(R)>=2]

    if verbose:
        print(f"input word = {word}\nsplits_l = {splits_l}\nswitch_l = {switch_l}")

    return switch_l


def replace_letter(word,verbose=False):
    """
    Input:  
        word:   word for which you will generate all possible words in vocab by replacing 1 character
    Output:
        replace_l:   list of all possible words obtained by replacing 1 character
    """

    letters= "abcdefghijklmnopqrstuvwxyz"
    
    splits_l =[(word[:i],word[i:]) for i in range(len(word)+1)]
    
    replace_l = [L + l + (R[1:] if len(R)> 1 else '') for L,R in splits_l if R for l in letters]
    replace_set = set(replace_l)
    replace_set.remove(word)

    replace_l = sorted(list(replace_set))

    if verbose:
        print(f"input word = {word}\nsplits_l = {splits_l}\nreplace_l = {replace_l}")

    return replace_l

def insert_letter(word,verbose=False):
    """
    Input:  
        word:   word for which you will generate all possible words in vocab by inserting 1 character
    Output:
        insert_l:   list of all possible words obtained by inserting 1 character
    """

    letters= "abcdefghijklmnopqrstuvwxyz"
    
    splits_l =[(word[:i],word[i:]) for i in range(len(word)+1)]

    insert_l = [L+l+R for L,R in splits_l if R for l in letters]

    if verbose:
        print(f"input word = {word}\nsplit_l = {splits_l}\ninsert_l = {insert_l}")

    return insert_l

def edit_one_letter(word,allow_switches=True):
    """
    Input: 
        word: string for which all possible words will be generated which are one edit away
    Output:
        edit_one_set:   set of all words with possible edits
    """
    
    edit_one_set =set()

    edit_one_set.update(delete_letter(word))
    edit_one_set.update(insert_letter(word))
    edit_one_set.update(replace_letter(word))
    

    if allow_switches:
        edit_one_set.update(switch_letter(word))
    

    return set(edit_one_set)


def edit_two_letters(word,allow_switches=True):
    """
    Input:
        word: input string/word
    Output:
        edit_two_set: set of string with all possible two edits
    """

    edit_two_set = set()

    edit_one = edit_one_letter(word,allow_switches=True)

    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w,allow_switches=True)
            edit_two_set.update(edit_two)
        
    return set(edit_two_set)


def get_word_correction(word,probs,vocab,n=2,verbose=False):
    """
    Input:
        word: user entered string to check for suggestions
        probs: dictionary of probability created earlier
        vocab: set of vocabulary
        n: number of possible words you want to get
    Output:
        n_best: top n most probable words 
    """
    suggestions =[]
    n_best =[]
    best_words = {}

    # here .intersection() checks that generated word exists in vocab or not
    if word in vocab:
        suggestions =list(word)
    suggestions = list( (word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(vocab)  ) 

    for i in suggestions:
        if i in vocab:
            best_words[i] = probs[i]
        else:
            best_words[i] =0
    
    best_words = sorted(best_words.items(),key=lambda x: x[1],reverse=True)


    n_best = best_words[:n]

    return n_best
    

def min_edit_distance(source,target,ins_cost=1,del_cost=1,replace_cost=2):
    """
    Input: 
        source: string you are starting with
        target: string you want to end with
        ins_cost,del_cost,replace_cost: cost of performing operation
    Output:
        D: matrix of rows (len(source)+1) and cols (len(target)+1) containing minimum edit distance
        med: minimum edit distance to convert from source to target
    """
    m = len(source)
    n = len(target)

    D = np.zeros((m+1,n+1),dtype=int)

    # for column 0,row 1 to m fill values with D[i-1,0]+del_cost(source[i])
    for row in range(1,m+1):
        D[row,0] = D[row-1,0]+del_cost
    
    # for row 0, column 1 t0 n fill values with D[0,j-1]+ins_cost(target[j])
    for col in range(1,m+1):
        D[0,col] = D[0,col-1]+ins_cost
    
    for i in range(1,m+1):
        for j in range(1,n+1):
            
            r_cost = replace_cost
            
            if source[i-1] == target[j-1]:
                r_cost = 0
            
            D[i,j] = min( D[i-1,j]+del_cost, D[i,j-1]+ins_cost, D[i-1,j-1]+r_cost )

    # minimum edit distance
    med = D[m,n]
            
    return D,med



def run_function(word):

    word_l = process_data("C:\\Users\\Jay\\Desktop\\google_10000.txt")
    vocab = set(word_l)
    
    word_count_dict = get_count(word_l)
    probs = get_prob(word_count_dict)

    
    x = get_word_correction(word,probs,vocab,n=10)
    
    return x


