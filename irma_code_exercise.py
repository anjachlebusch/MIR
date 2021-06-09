import csv
import os
import pandas as pd
from collections import defaultdict
from pathlib import Path

def csv_to_dict(file_path):
    if Path(file_path).exists() == False:
            print('Incorrect or not defined Path')
            return False
    else:
        dic={}
        lengList=[]
        f = open(file_path, "r")
        with f:
            reader=csv.reader(f)
            for row in reader:
                if len(row)==1:
                    key,value=row[0].split(";")
                    dic[key]= value  
                if len(row)==2:
                    key,value=row[0].split(";")
                    value= value+row[1]
                    dic[key]= value  
        f.close()
       
        return dic

    #  d = dict()
    #  with open(file_path, "r") as csv_file:
    #     if file_path==r"C:\Users\User\Documents\MIR\static\Irma data-20210525"+"\image_codes.csv":
    #      csv_reader = csv.DictReader(csv_file, delimiter=';')
    #      for lines in csv_reader:
    #             d[lines['1880']]=lines['1121-127-700-500']
 
    #     else:
    #         csv_reader = csv.DictReader(csv_file, delimiter=';')
    #         for lines in csv_reader:
    #             d[lines['0']]=lines['unspecified']
    



        
    # with open(file_path, newline='') as csvfile:
    #     data = csv.DictReader(csvfile)
    #     for row in data:
    #         print(row)
    # return data
    # Function to read in a csv file and create a dict based on the first two columns.

    # Parameters
    # ----------
    # - file_path : string
    #     The filepath to the CSV file.
    
    # Returns
    # -------
    # - csv_dict : dict
    #     The dict created from the CSV file.

    # Tipps
    # -------
    # - Read in the CSV file from the path
    # - For each row, add an entry to a dict (first column is key, second column is value)
    # - Return the dict
    # """
    
class IRMA:

    """
    Class to retrieve the IRMA code and information for a given file.
    """
    labels_long = ["Technical code for imaging modality", "Directional code for imaging orientation", "Anatomical code for body region examined", "Biological code for system examined"]
    labels_short = ["Imaging modality", "Imaging orientation", "Body region", "System"]

    def __init__(self, dir_path= 'static/Irma data-20210525'):
    
        """
        Constructor of an IRMA element.

        Parameters
        ----------
        - dir_path : string
            The path where the irma data is. There should be a "A.csv", "B.csv", "C.csv", "D.csv" and "image_codes.csv" file in the directory.

        Tipps
        -------
        - Create a dict for part A, B, C, and D of the IRMA code (user csv_to_dict(file_path))
        - Save the dicts (list) as class variable
        - Save "image_codes.csv" as dict in a class variable
        """
        
        A=csv_to_dict(dir_path+"\A.csv")
        B=csv_to_dict(dir_path+"\B.csv")
        C=csv_to_dict(dir_path+"\C.csv")
        D=csv_to_dict(dir_path+"\D.csv")


        self.dicts_list=[A,B,C,D]
        self.image_codes=csv_to_dict(dir_path+"\image_codes.csv")
  

    def get_irma(self, image_names):

        irma_codes=[]
        for i in range(len(image_names)):
            image=os.path.splitext(image_names[i])[0]
    
            try:
                irma_codes.append(self.image_codes[image])
            except:
                irma_codes.append(None)
        return irma_codes                

       
            
        """
        Function to retrieve irma codes for given image names.

        Parameters
        ----------
        - image_names : list
            List of image names.

        Returns
        -------
        - irma codes : list
            Retrieved irma code for each image in 'image_list'

        Tipps
        -------
        - Remove file extension and path from all names in image_names. Names should be in format like first column of 'image_codes.csv'
        - Use self.image_dict to convert names to codes. ('None' if no associated code can be found)
        - Return the list of codes
        
        """

      

    def decode_as_dict(self, code):
        decoded={}
        keys=code.split("-")
        
        
        for i in range(0,len(self.labels_short)):
            string=""
            keys_sublist=[]
            for j in range(0,len(keys[i])):
                string=string+keys[i][j]
                keys_sublist.append((self.dicts_list[i]).get(string))
            decoded[self.labels_short[i]]=keys_sublist
        return decoded
        """
        Function to decode an irma code to a dict.

        Parameters
        ----------
        - code : str
            String to decode.

        Returns
        -------
        - decoded : dict

        Tipps
        -------
        - Make use of 'labels_short'
        - Possible solution: {'Imaging modality': ['x-ray', 'plain radiography', 'analog', 'overview image'], ...}
        - Solution can look different
        """
        pass

    def decode_as_str(self, code):
        decoded=str(self.decode_as_dict(code))
        # decoded={}
        # keys=code.split("-")
        # for i in range(0,len(self.labels_long)):
        #     decoded[self.labels_long[i]]=(self.dicts_list[i]).get(keys[i])
        return decoded

        """
        Function to decode an irma code to a str.

        Parameters
        ----------
        - code : str
            String to decode.

        Returns
        -------
        - decoded : str
            List of decoded strings.

        Tipps
        -------
        - Make use of 'decode_as_dict'
        - Possible solution: ['Imaging modality: x-ray, plain radiography, analog, overview image', 'Imaging orientation: coronal, anteroposterior (AP, coronal), supine', 'Body region: abdomen, unspecified', 'System: uropoietic system, unspecified']
        - Solution can look different -> FLASK will use this representation to visualize the information on the webpage.
        """
        pass

if __name__ == '__main__':
    image_names = ["1880.png"]

    irma = IRMA()

    codes = irma.get_irma(image_names)
    print("Codes: ", codes)

    if codes is not None:
        code = codes[0]
        print("Dict: \n{}\n\n".format(irma.decode_as_dict(code)))
        print("String: \n{}\n\n".format(irma.decode_as_str(code)))

    '''
    Result could look like this:


    Codes:  ['1121-127-700-500']
    Dict:
    {'Imaging modality': ['x-ray', 'plain radiography', 'analog', 'overview image'], 'Imaging orientation': ['coronal', 'anteroposterior (AP, coronal)', 'supine'], 'Body region': ['abdomen', 'unspecified'], 'System': ['uropoietic system', 'unspecified']}


    String:
    ['Imaging modality: x-ray, plain radiography, analog, overview image', 'Imaging orientation: coronal, anteroposterior (AP, coronal), supine', 'Body region: abdomen, unspecified', 'System: uropoietic system, unspecified']
    '''