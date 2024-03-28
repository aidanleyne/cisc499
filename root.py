from flask import Flask, render_template, request, jsonify
from utility.individual_image_generation import generate_images
from utility.image_vector_gen import get_vector
from utility.lookup_box_utility import get_closest_vector

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_events', methods=['POST'])
def handle_data():
    data = request.get_json()
    myData = data['data']
    image_title = "test_phase_image.png"

    print("Received events from user typing")
    generate_images(myData, image_title)
    get_closest_vector(get_vector(image_title))

    return jsonify({'status': 'success'})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
