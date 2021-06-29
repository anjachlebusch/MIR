import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from preprocessing import preprocessing_main
from query import Query
from irma_code_exercise import IRMA
from relevance_feedback_idea import relevance_feedback
import relevance_feedback_idea

"""
This is the main file to run the medical information retrieval server.
The following dataset can be used to retrieve similar images: https://publications.rwth-aachen.de/record/667228
"""

database_path = "static/images/database/"

feeback_result = None
selected_image = None


app = Flask(__name__)
app.config['IMAGE_UPLOADS']='static/images/query'

query = Query(path_to_index= "outputresults.csv")
irma=IRMA()

elements_per_page = 10
page= 1

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    global selected_image
    return render_template("start.html", selected_image= selected_image)

@app.route("/selected_image", methods=['POST'])
def select_query_image():
     f=request.files['file']
     global selected_image
     selected_image=secure_filename(f.filename)
     f.save(os.path.join(APP_ROOT,app.config["IMAGE_UPLOADS"],selected_image))

     return render_template("start.html", selected_image= selected_image)

@app.route("/query_result", methods=['POST'])
def start_query(limit=elements_per_page):
    global query
    query.set_image_name(query_image_name=selected_image)
    query_result=query.run(limit)

    return visualize_query(query_result)

def visualize_query(query_result):
    global selected_image
    global irma
    image_names=[]
    image_distances=[]
    image_codes=[]
    irma_infos=[]

    for element in query_result:
        image_path=element[0].split("\\")
        image_names.append(image_path[-1])
        image_distances.append(element[1])
        image_codes=irma.get_irma(image_names)
        for i in range(len(image_codes)):
            code = image_codes[i]
            irma_infos.append(irma.decode_as_dict(code))
  
        
    return render_template("query_result.html", 
        zipped_input=zip([image_names[0]],[image_codes[0]],[irma_infos[0]]),
     zipped_results= zip(image_names[1:], image_distances[1:], image_codes[1:], irma_infos[1:]))

@app.route("/recalc", methods=['POST'])
def recalc_index():

    # TODO:

    return render_template("start.html", selected_image= selected_image)

@app.route("/new_page", methods=['POST'])
def new_page():
    global page
    page=page+1  
    render_template("query_result.html", page=page)
    return start_query(page*elements_per_page)


@app.route('/relevance_feedback', methods=['POST', 'GET'])
def relevance_feedback():
    global page
    global feeback_result
    global query
    page=1
    if request.method == 'POST':
        data=request.get_json()
        
        
        selected_images=data['si'].split(";")
        selected_images=selected_images[0:-1]

        not_selected_images=data['nsi'].split(";")
        not_selected_images=not_selected_images[0:-1]

      
        feeback_result= relevance_feedback_idea.relevance_feedback(query,selected_images,not_selected_images)
 
    
        return 'response',200 


    if request.method == 'GET':
        return visualize_query(feeback_result)

if __name__ == "__main__":
    app.run(port=4555, debug=True)
