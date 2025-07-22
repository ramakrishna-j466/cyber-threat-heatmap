from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/threats')
def get_threats():
    with open('data/threats.json') as f:
        data = json.load(f)
    return jsonify(data)
    
@app.route("/update")
def update_data():
    os.system("python fetch_data.py")
    return "Updated!"


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)




