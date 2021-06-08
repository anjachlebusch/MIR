from flask import Flask, render_template, request,redirect
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['IMAGE_UPLOADS']='static'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))




'''
Tutorial help: https://www.tutorialspoint.com/flask/flask_file_uploading.htm
'''

#app.config["IMAGE_UPLOADS"] = r"C:\Users\User\Documents\MIR\Flask exercise-20210511/static"

@app.route('/')
def start():
   return render_template('upload.html')
	
@app.route("/selected_image", methods=['POST'])
def select_query_image():
     f=request.files['file']
     filename=secure_filename(f.filename)
     f.save(os.path.join(APP_ROOT,app.config["IMAGE_UPLOADS"],filename))
 
     return render_template('show_image.html',query_file=filename)


		
if __name__ == '__main__':
   app.run(debug = True)