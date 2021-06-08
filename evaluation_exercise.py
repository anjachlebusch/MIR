from preprocessing import get_images_paths
import query
from irma_code_exercise import IRMA

import cv2
import sys
import numpy as np
from pathlib import Path
import csv
import os
from tqdm import tqdm


def count_codes(code_path ='static/Irma data-20210525/image_codes.csv'): 
    if Path(code_path).exists() == False:
        print('Incorrect or not defined Path')
        return ("error")
    else: 
        dict={}
        f=open(code_path, "r")
        with f:
            reader=csv.reader(f)
            for row in reader:
                if row[1] in dict.keys():
                    dict[row[1]]=dict[row[1]]+1
                else:
                    dict[row[1]]=1
        return dict
              
    
    """
    Counts the occurrence of each code in the given "CSV" file.

    Parameters
    ----------
    code_path : string
        Path to the csv file. Default= irma_data/image_codes.csv"
    Returns
    -------
    results : dict
        Occurrences of each code. Key is the code, and value the amount of occurrences.
    Task
    -------
        - If there is no code file -> Print error and return False [Hint: Path(*String*).exists()]
        - Open the code file
        - Read in CSV file [Hint: csv.reader()]
        - Iterate over every row of the CSV file
            - Make an entry in a dict
        - Close file
        - Return results
    """
    # TODO:



def precision_at_k(correct_prediction_list, k = None):
    if k==None:
        k==len(correct_prediction_list)
    elif k>len(correct_prediction_list):
        return("error")
    else:
        correct_prediction_list=correct_prediction_list[0:k]
    tp=0
    for i in correct_prediction_list:
        if i ==True:
            tp=tp+1
    return tp/k

    
    """
    Function to calculate the precision@k.

    Parameters
    ----------
    correct_prediction_list : list
        List with True/False values for the retrieved images.
    k : int
        K value.
    Returns
    -------
    precision at k : float
        The P@K for the given list.
    Task
    -------
        - If k is not defined -> k should be length of list
        - If k > length -> Error
        - If k < length -> cut off correct_prediction_list at k
        - Calculate precision for list
    Examples
    -------

        print("P@K: ", precision_at_k([True, True, True, False]))
        >>> P@K:  0.75

        print("P@K: ", precision_at_k([True, True, True, False], 2))
        >>> P@K:  1.0
    """
    #TODO:

def average_precision(correct_prediction_list, amount_relevant= None):
    if amount_relevant==None:
        amount_relevant=len(correct_prediction_list)
    else:
        for element in range(len(correct_prediction_list)):
            


    """
    Function to calculate the average precision.

    Parameters
    ----------
    correct_prediction_list : list
        List with True/False values for the retrieved images.
    amount_relevant : int
        Number of relevant documents for this query. Default is None.
    Returns
    -------
    average precision : float
        The average precision for the given list.
    Tasks
    -------
        - If amount_relevant is None -> amount_relvant should be the length of 'correct_prediction_list'
        - Iterate over 'correct_prediction_list'
            - Calculate p@k at each position
        - sum up values and divide by 'amount_relevant'
    Examples
    -------

        print("AveP: ", average_precision([True, True, True, False]))
        >>> P@AveP:  0.75

        print("AveP: ", average_precision([True, True, False, True], 3))
        >>> AveP:  0.9166666666666666
    """
    #TODO:
    pass

def mean_average_precision(limit = 10000):
    """
    Function to calcualte the mean average precision of the database.

    Parameters
    ----------
    limit : int
        Limit of the query. Default is None.
    Returns
    -------
    mean average precision : float
        The meanaverage precision of the selected approach on the database.
    Tasks
    -------
        - Create irma object and count codes.
        - Iterate over every image path (you can use 'tqdm' to check the run time of your for loop)
            - Create and run a query for each image
            - Compute a correct_prediction_list
            - Remove the first element (its the query image)
            - Compute AP (function) and save the value
        - Compute mean of APs
    """

    #TODO:
    pass

if __name__ == "__main__":
    test = [True, False, True, False]
    print("Examples with query results: ", str(test)) 
    print("P@K: ", precision_at_k(test, 3))
    print("AveP: ", average_precision(test, 3))

    result = mean_average_precision()
    print("\n\n")
    print("-"*50)
    print("Evaluation of the database")
    print("MAP: ", result)