#!/usr/bin/python3
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import base64
import logging
import atexit
from utils.ImageGenerator import ImageGenerator
from utils.database import Database
from utils.User import Profile
from models import taunet, fpnet

###LOGGING SETUP###
logging.basicConfig(filename="flaskServer.log",
                    format='%(asctime)s : %(name)s : %(message)s',
                    filemode='a',
                    level=logging.INFO)
logger = logging.getLogger()

### RESOURCE SETUP ###
app = Flask(__name__)
db = Database(256)
db.import_database()
ig = ImageGenerator('temp')
logging.info("Resources set-up")

#generates the array based onf iles
def generate_arr():
    #generate arrays based on img and txt
    fp = fpnet.generate('temp/temp.png').tolist()
    tn = taunet.generate('temp/temp.txt').tolist()
    
    #combine the two arrays for 256-length
    arr = np.array(fp + tn)
    return (arr/np.linalg.norm(arr)).tolist()

#closes db and preforms other exit tasks
def exit_handler():
    print("Processing Exit Tasks...")
    db.export_database()
    print("Program is exiting.")
    
#handle program exit
atexit.register(exit_handler)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    exit_handler()
    print('Server shutting down...')
    return

#routes homepage to the index html file
@app.route('/')
def home():
    return render_template('index.html')

#gets the events array from front end and sends to python file to be generated and saved
@app.route('/get_events', methods=['POST'])
def handle_data():
    #send user data to pandas df
    user_data = pd.DataFrame(request.get_json())
    
    #create the phase image
    ig.compute(passed_data=user_data)

    return jsonify({'status': 'success'})

#API call to send the image to be displayed on the frontend
@app.route('/get_image')
def get_image():
    with open('temp/temp.png', 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return jsonify(image=encoded_string)

#adds new user to the database
@app.route('/add_user', methods=['POST'])
def add_user():
    id = request.json['id']
    for vec in db.db.values():
        if vec.profile is not None and vec.profile.id == id:
            return jsonify({'status': 'exists'})
        
    arr = generate_arr()
    pf = Profile(id)
    db.insert(arr, profile=pf)
    return jsonify({'status': 'added'})

@app.route('/lookup', methods=['GET'])
def lookup():
    arr = generate_arr()
    result = db.find(arr)
    id = result[0][0]
    unsalted_distance = result[0][1]
    id_salted = result[1][0]
    salted_distance = result[1][1]
    if id > -1:
        return jsonify({
            'unsalted': str(db.db[id].profile.id),
            'salted' : str(db.salted_db[id_salted].profile.id),
            'unsalted_distance' : str(unsalted_distance),
            'salted_distance' : str(salted_distance)
            })
    return jsonify({
        'unsalted' : 'None',
        'salted' : 'None'
        })

@app.route('/get_num_entries', methods=['GET'])
def get_num_entries():
    return jsonify({'unsalted' : len(db.db), 'salted' : len(db.salted_db)})

# Run the application
if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')
