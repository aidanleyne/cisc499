from flask import Flask, render_template, request, jsonify
from lookup.database import Database
from utils.ImageGenerator import ImageGenerator
import pandas as pd
import base64
import logging

###LOGGING SETUP###
logging.basicConfig(filename="flaskServer.log",
                    format='%(asctime)s : %(name)s : %(message)s',
                    filemode='a',
                    level=logging.INFO)
logger = logging.getLogger()

### RESOURCE SETUP ###
app = Flask(__name__)
db = Database(256)
ig = ImageGenerator('temp')
logging.info("Resources set-up")

IMG = None

#routes homepage to the index html file
@app.route('/')
def home():
    return render_template('index.html')

#gets the events array from front end and sends to python file to be generated and saved
@app.route('/get_events', methods=['POST'])
def handle_data():
    user_data = pd.DataFrame(request.get_json())
    print(user_data)
    
    #create the phase image
    ig.compute(passed_data=user_data)

    #generate arrays based on 

    print("Received events from user typing")

    #generate_images(myData, image_title)
    #get_closest_vector(get_vector(image_title))

    return jsonify({'status': 'success'})


@app.route('/get_image')
def get_image():
    with open('temp/temp.png', 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return jsonify(image=encoded_string)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
