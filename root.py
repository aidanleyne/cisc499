from flask import Flask, render_template, request, jsonify
from image_generator_dummy import generate_images

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_events', methods=['POST'])
def handle_data():
    data = request.get_json()
    myData = data['data']
    print("Data received from JavaScript")
    generate_images(myData)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
