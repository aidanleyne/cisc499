from flask import Flask, render_template, request, jsonify
from lookup.database import Database
from utils.ImageGenerator import ImageGenerator
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

#routes homepage to the index html file
@app.route('/')
def home():
    return render_template('index.html')

#gets the events array from front end and sends to python file to be generated and saved
@app.route('/get_events', methods=['POST'])
def handle_data():
    data = request.get_json()
    user_data = data['data']
    print(user_data)
    image_title = "test_phase_image.png"

    print("Received events from user typing")
    #generate_images(myData, image_title)
    #get_closest_vector(get_vector(image_title))

    return jsonify({'status': 'success'})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
