from cv2 import cv2
import csv
def relevance_feedback(self, selected_images, not_selected_images, limit):
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
    relevant_feature=get_feature_vector(selected_images)
    non_relevant=get_feature_vector(not_selected_images)
    
    modified_features=rocchio(self.query.features,relevant_feature,non_relevant)
    self.query_features=modified_features
    self.feeback_result=self.query.run()
    return self.feeback_result[0:limit]
    

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
    f = open('static/index.csv', "r")
    with f:
        reader=csv.reader(f)
        for row in reader:
            data.append(row)
    f.close()

    for name in image_names:
        for images in data:
            if ((images[0].split('\\'))[1]==name):
               # path=images.pop(images[0])
                features.append(images[-1])
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

    vector_a=a*original_query

    for element in relevant:
        sum_r=[i + j for i, j in zip(sum_r, element)]
    vector_b=[b*(1/len(relevant))*i for i in sum_r]   

    
    for element in non_relevant:
        sum_nr=[i + j for i, j in zip(sum_nr, element)]
    vector_c=[c*(1/len(non_relevant))*i for i in sum_nr]

    features=[i + j - k for i, j, k in zip(vector_a,vector_b,vector_c)]

    return features