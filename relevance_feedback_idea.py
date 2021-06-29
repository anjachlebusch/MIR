from cv2 import cv2
import csv
from query import Query
from searcher import Searcher
def relevance_feedback(self, selected_images, not_selected_images, limit=10):
    """
    Function to start a relevance feedback query.
    Parameters
    ----------
    selected_images : list
        List of selected images.
    not_selected_images : list
        List of not selected images.
    limit : int
        Amount of results that will be retrieved. Default: 10.
    Returns
    -------
    - results : list
        List with the 'limit' first elements of the 'results' list. 
    """
    relevant_feature=get_feature_vector(self,selected_images)
    non_relevant=get_feature_vector(self,not_selected_images)


    modified_features=rocchio(self.features,relevant_feature,non_relevant)

    searcher=Searcher("outputresults.csv")
    results=searcher.search(modified_features)

    return results[0:limit]
    

    # get relavent and non_revant feature vectors

    # rocchio

    # run new query

    # update the current features , so repeated "relavance feedback" has an effect

    # return our (limited) results

def get_feature_vector(self, image_names):
    """
    Function to get features from 'index' file for given image names.
    Parameters
    ----------
    image_names : list
        List of images names.
    Returns
    -------
    - features : list
        List with of features.
    """
    data=[]
    features=[]
    f = open('outputresults.csv', "r")
    with f:
        reader=csv.reader(f)
        for row in reader:
            data.append(row)
    f.close()

    #get the features of the images in the image_names list from the csv file
    for name in image_names:
        for images in data:
            
            if ((images[0].split('\\'))[-1]==name):
                tempIm=images[1:]

                for i in range(len(tempIm)):
                    tempIm[i]=float(tempIm[i])
                features.append(tempIm)
    return features


        
def rocchio(original_query, relevant, non_relevant, a = 1, b = 0.8, c = 0.1):
    """
    Function to adapt features with rocchio approach.

    Parameters
    ----------
    original_query : list
        Features of the original query.
    relevant : list
        Features of the relevant images.
    non_relevant : list
        Features of the non relevant images.
    a : int
        Rocchio parameter.
    b : int
        Rocchio parameter.
    c : int
        Rocchio parameter.
    Returns
    -------
    - features : list
        List with of features.
    """
    features=[]
    sum_r=[]
    sum_nr=[]
    vector_c=[]
    vector_b=[]
    vector_a=[]
    

    for element in original_query:
        vector_a.append(element*a)

    for element in relevant:
        if len(sum_r)==0:
                sum_r=element
        else:
            for j in range(len(element)):
                sum_r[j]=sum_r[j]+element[j]
       
    for i in range(len(sum_r)):
        vector_b.append(b/len(relevant)*float(sum_r[i]))
        
      

    
    for element in non_relevant:
        if len(sum_nr)==0:
            sum_nr=element
        else:
            for j in range(len(element)):
                sum_nr[j]=sum_nr[j]+element[j]
    
    for i in range(len(sum_nr)):
        vector_c.append(c/len(non_relevant)*sum_nr[i])

    
    for i,j,k in zip(vector_a,vector_b,vector_c):
        features.append(i+j-k)

    return features