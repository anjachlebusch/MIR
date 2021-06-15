from cv2 import cv2
import csv
from query import Query
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

    f=open('selectedOutput.csv',"w")
    with f:
        writer=csv.writer(f)
        for i in range(len(selected_images)):
            relevant_featureStr= ','.join(map(str, relevant_feature))
            writer.writerow(selected_images[i]+";"+relevant_featureStr)
    f.close

    modified_features=rocchio(self.features,relevant_feature,non_relevant)


    

    query=Query("selectedOutput.csv")
    query.set_image_name(self.query_image_name)
    self.features=modified_features
    result=query.run()
    
    return result[0:limit]
    

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

    for name in image_names:
        for images in data:
            featureListFl=[]
            print(images[0])
            
            if ((images[0].split('\\'))[-1]==name):
                path=images.pop(0)

                for element in images:
                    element=float(element)
                features.append(images)
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
    
   # for i,j,k in zip(vector_a,vector_b,vector_c):
    #    features.append(i+j-k)
    features=[i + j - k for i, j, k in zip(vector_a,vector_b,vector_c)]

    return features