from flask import Flask, render_template, request, jsonify
from utils import predict_from_descriptor

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    descriptors = data.get('descriptors', [])
    results = [predict_from_descriptor(d) for d in descriptors]
    return jsonify([
        {'sim': sim, 'iq': iq, 'label': label}
        for sim, iq, label in results
    ])

if __name__ == '__main__':
    app.run()
