from flask import Flask, jsonify

app = Flask(__name__)
counter = 0

@app.route('/hello')
def hello():
    global counter
    counter += 1
    return jsonify(message="Hello from backend", iteration=counter)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
