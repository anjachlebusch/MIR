import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from preprocessing import preprocessing_main
from query import Query
from irma_code_exercise import IRMA

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
    query_result=query.run()

    return visualize_query(query_result)

def visualize_query(query_result):
    global selected_image
    global irma
    image_names=[]
    image_distances=[]
    image_codes=[]
    irma_infos=[]
    input_code= "hi"
    input_info= "hallo"
    for element in query_result:
        print(element)
        image_path=element[0].split("\\")
        image_names.append(image_path[1])
        image_distances.append(element[1])
        print(irma.get_irma(image_names))
        image_codes=irma.get_irma(image_names)
        for i in range(len(image_codes)):
            code = image_codes[i]
            print("Dict: \n{}\n\n".format(irma.decode_as_dict(code)))
            print("String: \n{}\n\n".format(irma.decode_as_str(code)))
            irma_infos.append(irma.decode_as_dict(code))
  
        
    return render_template("query_result.html", 
        zipped_input=zip([selected_image],input_info),#, input_code, input_info),
     zipped_results= zip(image_names, image_distances, image_codes, irma_infos))

@app.route("/recalc", methods=['POST'])
def recalc_index():

    # TODO:

    return render_template("start.html", selected_image= selected_image)

@app.route("/new_page", methods=['POST'])
def new_page():
    global page
    page+=1  
    render_template("query_result.html", page=page)
    return start_query(page*elements_per_page)


@app.route('/relevance_feedback', methods=['POST', 'GET'])
def relevance_feedback():
    global feeback_result
    global query
    if request.method == 'POST':
        selected_images, not_selected_images=request.form["selected_images, not_selected_images"]
        for element in selected_images:
            print("Selected Image: "+element)
        for element in not_selected_images:
            print("Not selected Image: "+element)
        
    
        # TODO:
        


    if request.method == 'GET':
        selected_images, not_selected_images=request.form.get("selected_images"),request.form.get("not_selected_images")
        print("Selected Image: ",selected_images)
        print("Länge Selectes Images: "+len(selected_images))

        for element in selected_images:
            print("Selected Image: ",element)
        for element in not_selected_images:
            print("Not selected Image: ",element)
        
        
        feeback_result= relevance_feedback(selected_images,not_selected_images,10)
        return visualize_query(feeback_result)


    #if request.method == 'GET':
     #   return visualize_query(feeback_result)

if __name__ == "__main__":
    app.run(port=4555, debug=True)
