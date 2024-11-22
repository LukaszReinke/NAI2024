import numpy as np
from scipy.sparse import data
from sklearn.metrics.pairwise import cosine_similarity

# Compute the Euclidean distance score between user1 and user2 
def euclidean_score(dataset, user1, user2):
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    # Movies rated by both user1 and user2
    common_movies = {} 

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    # If there are no common movies between the users, 
    # then the score is 0 
    if len(common_movies) == 0:
        return 0

    squared_diff = [] 

    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))
        
    return 1 / (1 + np.sqrt(np.sum(squared_diff))) 

#implementacjia liczenia kata miedzy 2 punktami
def cosing_score(dataset, user1, user2):
    common_movies = {} 
    #sprawdzamy czy user1 i user2 maja takie same filmy
    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    # If there are no common movies between the users, 
    # then the score is 0 
    if len(common_movies) == 0:
        return 0
    
    ##licznik
    cosine_numerator  = []
    #mianownik
    cosine_denominator_user1 = []
    cosine_denominator_user2 = []
    
    for item in dataset[user1]:
        if item in dataset[user2]:
            cosine_numerator.append(dataset[user1][item]*dataset[user2][item])
            
    for item in dataset[user1]:
        if item in dataset[user2]:
            cosine_denominator_user1.append(np.square(dataset[user1][item]))
            
    for item in dataset[user1]:
        if item in dataset[user2]:
            cosine_denominator_user2.append(np.square(dataset[user2][item]))
            
    #wzor na cos kata miedzy 2 punktami mamy z https://en.wikipedia.org/wiki/Cosine_similarity
    return np.sum(cosine_numerator)/(np.sqrt(np.sum(cosine_denominator_user1)) * np.sqrt(np.sum(cosine_denominator_user2)))
    
    
